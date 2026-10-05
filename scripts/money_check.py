#!/usr/bin/env python3
"""Are the money controls at AWS still what the owner set up?

The owner's rule (CLAUDE.md §1, DECISIONS D10): nothing may raise spend, and
that must be protected at the provider, not just written down. On 2026-10-05
the owner set up four controls, and an audit found the Polly key had been able
to run 100,000-character jobs all year. This checks every control is still in
place. It runs in every shift, using a read-only key whose policy denies every
billable call:

    1. the Polly key may only call polly:SynthesizeSpeech
    2. a monthly all-services cost budget at or under the owner's line
    3. that budget automatically denies Polly to the key when it is spent
    4. a CloudWatch alarm on Polly characters per hour, emailing a confirmed address

It also reports this month's spend, which is Finance's ledger.

    venv/bin/python scripts/money_check.py             # exit 1 on drift
    venv/bin/python scripts/money_check.py --escalate  # and queue an issue for the owner

Credentials: AWS_READONLY_ACCESS_KEY_ID and AWS_READONLY_SECRET_ACCESS_KEY (the
shift's secret), or else AWS_PROFILE (locally, `reddit-digest-readonly`).
Never the Polly keys. It refuses to run as any identity other than the
read-only user, so it cannot be pointed at a key that could spend.

Exit codes: 0 all intact, 1 drift found, 2 could not check.
"""
import json
import os
import subprocess
import sys
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

READONLY_USER = "claude-readonly"
POLLY_USER = "polly"
POLLY_ALLOWED = {"polly:SynthesizeSpeech"}
# The owner's line. Raising either number weakens a cost control, which needs
# the owner (CLAUDE.md §4); guardrails.yml fails a push that raises them.
BUDGET_MAX_USD = 3.0
ALARM_MAX_CHARS_PER_HOUR = 10000
ALARM_REGION = "us-west-2"
# Production spends about $0.90/month. Past this share of the budget, spend has
# left its usual line -- not drift, but something Finance must explain.
SPEND_WARN_SHARE = 0.5
POLLY_DENY = {"polly:*", "polly:SynthesizeSpeech", "*"}


def _list(x):
    return [x] if isinstance(x, (str, dict)) else list(x or [])


def _doc(raw):
    """IAM policy documents arrive decoded from boto3, URL-encoded from the raw API."""
    return json.loads(urllib.parse.unquote(raw)) if isinstance(raw, str) else raw


def key_scope(iam):
    problems = []
    attached = iam.list_attached_user_policies(UserName=POLLY_USER)["AttachedPolicies"]
    if attached:
        problems.append("managed policies attached: "
                        + ", ".join(p["PolicyName"] for p in attached))
    groups = iam.list_groups_for_user(UserName=POLLY_USER)["Groups"]
    if groups:
        problems.append("in groups (which can grant more): "
                        + ", ".join(g["GroupName"] for g in groups))
    allowed, names = set(), iam.list_user_policies(UserName=POLLY_USER)["PolicyNames"]
    for name in names:
        doc = _doc(iam.get_user_policy(UserName=POLLY_USER, PolicyName=name)["PolicyDocument"])
        for st in _list(doc.get("Statement")):
            if st.get("Effect") == "Allow":
                allowed |= set(_list(st.get("Action")))
    extra = sorted(allowed - POLLY_ALLOWED)
    if extra:
        problems.append("allows more than SynthesizeSpeech: " + ", ".join(extra))
    if "polly:SynthesizeSpeech" not in allowed and not extra:
        problems.append("cannot call polly:SynthesizeSpeech, so uploads will fail")
    active = [k for k in iam.list_access_keys(UserName=POLLY_USER)["AccessKeyMetadata"]
              if k.get("Status") == "Active"]
    if len(active) > 1:
        problems.append(f"{len(active)} active access keys (expected 1)")
    detail = f"only polly:SynthesizeSpeech ({', '.join(names) or 'no inline policy'}); " \
             f"{len(active)} active key"
    return ("Polly key scope", not problems, "; ".join(problems) or detail)


def _all_services(b):
    return not b.get("CostFilters") and not b.get("FilterExpression")


def budget(budgets, account):
    found = [b for b in budgets.describe_budgets(AccountId=account).get("Budgets", [])
             if b.get("BudgetType") == "COST" and b.get("TimeUnit") == "MONTHLY"]
    good = [b for b in found if _all_services(b)
            and float(b["BudgetLimit"]["Amount"]) <= BUDGET_MAX_USD]
    if good:
        b = good[0]
        return ("Budget", True, f"\"{b['BudgetName']}\" ${float(b['BudgetLimit']['Amount']):.2f}"
                                f"/month, all services"), b
    if found:
        why = "; ".join(f"\"{b['BudgetName']}\" ${float(b['BudgetLimit']['Amount']):.2f}"
                        + ("" if _all_services(b) else " (filtered to some services)")
                        for b in found)
        return ("Budget", False, f"no all-services budget at or under ${BUDGET_MAX_USD:.2f}: {why}"), None
    return ("Budget", False, "no monthly cost budget exists"), None


def _denies_polly(iam, arn):
    try:
        version = iam.get_policy(PolicyArn=arn)["Policy"]["DefaultVersionId"]
        doc = _doc(iam.get_policy_version(PolicyArn=arn, VersionId=version)
                   ["PolicyVersion"]["Document"])
    except Exception as e:                   # unreadable is not the same as safe
        return False, f"could not read {arn.split('/')[-1]}: {type(e).__name__}"
    for st in _list(doc.get("Statement")):
        if st.get("Effect") == "Deny" and POLLY_DENY & set(_list(st.get("Action"))):
            return True, ""
    return False, f"{arn.split('/')[-1]} does not deny Polly"


def budget_action(budgets, iam, account, b):
    if b is None:
        return ("Budget action", False, "no qualifying budget to attach it to")
    actions = budgets.describe_budget_actions_for_budget(
        AccountId=account, BudgetName=b["BudgetName"]).get("Actions", [])
    reasons = []
    for a in actions:
        target = (a.get("Definition") or {}).get("IamActionDefinition") or {}
        why = []
        if a.get("ActionType") != "APPLY_IAM_POLICY":
            why.append(f"type {a.get('ActionType')}")
        if a.get("ApprovalModel") != "AUTOMATIC":
            why.append("needs manual approval")
        if POLLY_USER not in (target.get("Users") or []):
            why.append(f"does not target user {POLLY_USER}")
        t = a.get("ActionThreshold") or {}
        if t.get("ActionThresholdType") == "PERCENTAGE" and float(t.get("ActionThresholdValue", 0)) > 100:
            why.append(f"fires only at {t['ActionThresholdValue']}%")
        ok, msg = _denies_polly(iam, target.get("PolicyArn", "")) if target.get("PolicyArn") \
            else (False, "no policy to apply")
        if not ok:
            why.append(msg)
        if why:
            reasons.append("; ".join(why))
            continue
        if a.get("Status") != "STANDBY":
            return ("Budget action", False, f"has fired (status {a.get('Status')}): Polly is "
                    "denied to the key, so uploads cannot narrate until the owner reverses it")
        return ("Budget action", True, f"denies Polly to user {POLLY_USER} at "
                f"{t.get('ActionThresholdValue', '?')}% of actual spend, automatically; standby")
    return ("Budget action", False, "; ".join(reasons) or "no action on the budget")


def alarm(cloudwatch, sns):
    alarms = [a for a in cloudwatch.describe_alarms().get("MetricAlarms", [])
              if a.get("Namespace") == "AWS/Polly" and a.get("MetricName") == "RequestCharacters"]
    if not alarms:
        return ("Alarm", False, f"no alarm on Polly characters in {ALARM_REGION}")
    reasons = []
    for a in alarms:
        why = []
        if a.get("Statistic") != "Sum":
            why.append(f"statistic {a.get('Statistic')}")
        if float(a.get("Threshold", 1e12)) > ALARM_MAX_CHARS_PER_HOUR * a.get("Period", 3600) / 3600:
            why.append(f"threshold {a.get('Threshold'):.0f} per {a.get('Period')}s is too high")
        if not a.get("ActionsEnabled"):
            why.append("actions disabled")
        confirmed = False
        for arn in a.get("AlarmActions", []):
            if ":sns:" not in arn:
                continue
            subs = sns.list_subscriptions_by_topic(TopicArn=arn).get("Subscriptions", [])
            confirmed |= any(s.get("SubscriptionArn", "").startswith("arn:") for s in subs)
        if not confirmed:
            why.append("no confirmed email subscription")
        if why:
            reasons.append(f"{a['AlarmName']}: " + "; ".join(why))
            continue
        if a.get("StateValue") == "ALARM":
            return ("Alarm", False, f"{a['AlarmName']} is firing: Polly usage is above "
                    f"{a.get('Threshold'):.0f} characters in an hour")
        return ("Alarm", True, f"{a['AlarmName']}, over {a.get('Threshold'):.0f} characters "
                f"per {a.get('Period', 3600) // 60} min, email confirmed (state {a.get('StateValue')})")
    return ("Alarm", False, "; ".join(reasons))


def spend(b):
    """This month's spend against the budget -- Finance's ledger line."""
    if b is None:
        return ("Spend", False, "unknown: no qualifying budget")
    limit = float(b["BudgetLimit"]["Amount"])
    calc = b.get("CalculatedSpend") or {}
    actual = float((calc.get("ActualSpend") or {}).get("Amount", 0))
    forecast = (calc.get("ForecastedSpend") or {}).get("Amount")
    line = f"${actual:.2f} so far this month" + \
           (f" (forecast ${float(forecast):.2f})" if forecast is not None else "") + \
           f" of ${limit:.2f}"
    if actual >= SPEND_WARN_SHARE * limit:
        return ("Spend", False, f"{line}: above the usual line of about $0.90")
    if forecast is not None and float(forecast) > limit:
        return ("Spend", False, f"{line}: forecast to exceed the budget")
    return ("Spend", True, line)


def evaluate(c, account):
    results = [key_scope(c["iam"])]
    result, b = budget(c["budgets"], account)
    results += [result, budget_action(c["budgets"], c["iam"], account, b),
                alarm(c["cloudwatch"], c["sns"]), spend(b)]
    return results


def clients():
    """Read-only clients, or None when no read-only credentials are present."""
    import boto3
    key = os.environ.get("AWS_READONLY_ACCESS_KEY_ID")
    secret = os.environ.get("AWS_READONLY_SECRET_ACCESS_KEY")
    if key and secret:
        session = boto3.Session(aws_access_key_id=key, aws_secret_access_key=secret)
    elif os.environ.get("AWS_PROFILE"):
        session = boto3.Session(profile_name=os.environ["AWS_PROFILE"])
    else:
        return None
    return {"sts": session.client("sts", region_name=ALARM_REGION),
            "iam": session.client("iam"),
            "budgets": session.client("budgets", region_name="us-east-1"),
            "cloudwatch": session.client("cloudwatch", region_name=ALARM_REGION),
            "sns": session.client("sns", region_name=ALARM_REGION)}


def identity_ok(arn):
    return arn.endswith(f":user/{READONLY_USER}")


def escalate(failed):
    body = "## What drifted\n\n" + "\n".join(f"- **{n}:** {d}" for n, _, d in failed) + \
           "\n\nFound by `scripts/money_check.py`, which compares the AWS money controls " \
           "with what the owner set up on 2026-10-05 (TECH_DEBT.md, dry-run item)."
    return subprocess.run(
        [sys.executable, os.path.join(ROOT, "scripts", "escalate.py"),
         "--title", "A money control at AWS has drifted", "--key", "money-controls-drift",
         "--labels", "needs-owner,guardrail",
         "--recommend", "Restore the control in the AWS console; ask a session to "
                        "re-run the check to confirm."],
        input=body, text=True, capture_output=True)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    try:
        c = clients()
    except Exception as e:
        print(f"Could not check the money controls: {type(e).__name__}: {e}")
        return 2
    if c is None:
        print("Could not check the money controls: no read-only AWS credentials "
              "(AWS_READONLY_ACCESS_KEY_ID, or AWS_PROFILE=reddit-digest-readonly locally).")
        return 2
    try:
        me = c["sts"].get_caller_identity()
        if not identity_ok(me["Arn"]):
            print(f"Refusing to run as {me['Arn']}: only {READONLY_USER} may run this check.")
            return 2
        results = evaluate(c, me["Account"])
    except Exception as e:
        print(f"Could not check the money controls: {type(e).__name__}: {e}")
        return 2

    print(f"MONEY CONTROLS (AWS account {me['Account'][:4]}…)")
    for name, ok, detail in results:
        print(f"  {'ok   ' if ok else 'DRIFT'} {name}: {detail}")
    failed = [r for r in results if not r[1]]
    if not failed:
        return 0
    if "--escalate" in argv:
        r = escalate(failed)
        print("\n" + (r.stdout.strip() or r.stderr.strip()))
        print("Commit and push .escalations/ so the issue reaches the owner.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
