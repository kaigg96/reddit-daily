"""The money check compares the AWS controls with what the owner set up on
2026-10-05. Each test starts from that exact setup -- read back live the same
day -- and changes one thing, which the check must catch."""
import copy
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts import money_check as mc

ACCOUNT = "851725656965"
SYNTH_ONLY = {"Version": "2012-10-17", "Statement": [{
    "Effect": "Allow", "Action": "polly:SynthesizeSpeech", "Resource": "*",
    "Condition": {"StringEquals": {"aws:RequestedRegion": "us-west-2"}}}]}
DENY = {"Version": "2012-10-17", "Statement": [{"Effect": "Deny", "Action": "polly:*", "Resource": "*"}]}
TOPIC = f"arn:aws:sns:us-west-2:{ACCOUNT}:Default_CloudWatch_Alarms_Topic"

LIVE = {
    "attached": [], "groups": [], "inline": {"PollySynthesizeOnly": SYNTH_ONLY},
    "keys": [{"Status": "Active"}],
    "budgets": [{"BudgetName": "Polly budget", "BudgetType": "COST", "TimeUnit": "MONTHLY",
                 "BudgetLimit": {"Amount": "3.0", "Unit": "USD"},
                 "CalculatedSpend": {"ActualSpend": {"Amount": "0.135"},
                                     "ForecastedSpend": {"Amount": "0.96"}}}],
    "actions": [{"ActionType": "APPLY_IAM_POLICY", "ApprovalModel": "AUTOMATIC",
                 "Status": "STANDBY",
                 "ActionThreshold": {"ActionThresholdValue": 100.0,
                                     "ActionThresholdType": "PERCENTAGE"},
                 "Definition": {"IamActionDefinition": {
                     "PolicyArn": f"arn:aws:iam::{ACCOUNT}:policy/DenyPolicy",
                     "Users": ["polly"]}}}],
    "policies": {f"arn:aws:iam::{ACCOUNT}:policy/DenyPolicy": DENY},
    "alarms": [{"AlarmName": "Polly-Usage-Exceeding-10k", "Namespace": "AWS/Polly",
                "MetricName": "RequestCharacters", "Statistic": "Sum", "Period": 3600,
                "Threshold": 10000.0, "ActionsEnabled": True, "AlarmActions": [TOPIC],
                "StateValue": "INSUFFICIENT_DATA"}],
    "subs": {TOPIC: [{"SubscriptionArn": f"{TOPIC}:4a20fcd9"}]},
}


class Fake:
    """One object standing in for the iam, budgets, cloudwatch and sns clients."""

    def __init__(self, state):
        self.s = state

    def list_attached_user_policies(self, UserName):
        return {"AttachedPolicies": self.s["attached"]}

    def list_groups_for_user(self, UserName):
        return {"Groups": self.s["groups"]}

    def list_user_policies(self, UserName):
        return {"PolicyNames": list(self.s["inline"])}

    def get_user_policy(self, UserName, PolicyName):
        return {"PolicyDocument": self.s["inline"][PolicyName]}

    def list_access_keys(self, UserName):
        return {"AccessKeyMetadata": self.s["keys"]}

    def describe_budgets(self, AccountId):
        return {"Budgets": self.s["budgets"]}

    def describe_budget_actions_for_budget(self, AccountId, BudgetName):
        return {"Actions": self.s["actions"]}

    def get_policy(self, PolicyArn):
        return {"Policy": {"DefaultVersionId": "v1"}}

    def get_policy_version(self, PolicyArn, VersionId):
        return {"PolicyVersion": {"Document": self.s["policies"][PolicyArn]}}

    def describe_alarms(self):
        return {"MetricAlarms": self.s["alarms"]}

    def list_subscriptions_by_topic(self, TopicArn):
        return {"Subscriptions": self.s["subs"].get(TopicArn, [])}


def check(change=None):
    state = copy.deepcopy(LIVE)
    if change:
        change(state)
    f = Fake(state)
    return {name: (ok, detail) for name, ok, detail in
            mc.evaluate({"iam": f, "budgets": f, "cloudwatch": f, "sns": f}, ACCOUNT)}


def failed(change):
    return {n: d for n, (ok, d) in check(change).items() if not ok}


def test_the_owners_setup_passes():
    assert failed(None) == {}


def test_the_key_as_it_was_before_the_audit_is_caught():
    """polly:* allowed 100,000-character async jobs for a year."""
    out = failed(lambda s: s["inline"].update(PollySynthesizeOnly={
        "Statement": [{"Effect": "Allow", "Action": ["polly:*"], "Resource": ["*"]}]}))
    assert "polly:*" in out["Polly key scope"]


def test_a_managed_policy_or_group_is_caught():
    out = failed(lambda s: (s["attached"].append({"PolicyName": "AmazonPollyFullAccess"}),
                            s["groups"].append({"GroupName": "admins"})))
    assert "AmazonPollyFullAccess" in out["Polly key scope"] and "admins" in out["Polly key scope"]


def test_a_key_that_cannot_synthesize_is_caught():
    out = failed(lambda s: s["inline"].clear())
    assert "uploads will fail" in out["Polly key scope"]


def test_a_raised_or_filtered_budget_is_caught():
    assert "Budget" in failed(lambda s: s["budgets"][0]["BudgetLimit"].update(Amount="50"))
    out = failed(lambda s: s["budgets"][0].update(CostFilters={"Service": ["Amazon Polly"]}))
    assert "filtered" in out["Budget"]


def test_an_action_needing_manual_approval_or_not_denying_is_caught():
    assert "manual" in failed(lambda s: s["actions"][0].update(ApprovalModel="MANUAL"))["Budget action"]
    out = failed(lambda s: s["policies"].update({
        f"arn:aws:iam::{ACCOUNT}:policy/DenyPolicy": {"Statement": [
            {"Effect": "Allow", "Action": "polly:*", "Resource": "*"}]}}))
    assert "does not deny Polly" in out["Budget action"]


def test_a_fired_action_is_reported_as_polly_being_denied():
    out = failed(lambda s: s["actions"][0].update(Status="EXECUTION_SUCCESS"))
    assert "uploads cannot narrate" in out["Budget action"]


def test_a_missing_alarm_or_unconfirmed_email_is_caught():
    assert "no alarm" in failed(lambda s: s["alarms"].clear())["Alarm"]
    out = failed(lambda s: s["subs"].update({TOPIC: [{"SubscriptionArn": "PendingConfirmation"}]}))
    assert "no confirmed email" in out["Alarm"]


def test_spend_above_the_usual_line_is_reported():
    out = failed(lambda s: s["budgets"][0]["CalculatedSpend"]["ActualSpend"].update(Amount="1.80"))
    assert "above the usual line" in out["Spend"]


def test_only_the_read_only_user_may_run_it():
    assert mc.identity_ok(f"arn:aws:iam::{ACCOUNT}:user/claude-readonly")
    assert not mc.identity_ok(f"arn:aws:iam::{ACCOUNT}:user/polly")
    assert not mc.identity_ok(f"arn:aws:iam::{ACCOUNT}:root")


def test_no_credentials_means_could_not_check(monkeypatch):
    for k in ("AWS_READONLY_ACCESS_KEY_ID", "AWS_READONLY_SECRET_ACCESS_KEY", "AWS_PROFILE"):
        monkeypatch.delenv(k, raising=False)
    assert mc.main([]) == 2


def test_the_owners_line_is_not_raised():
    """guardrails.yml checks the same numbers on every push."""
    assert mc.BUDGET_MAX_USD <= 3.0 and mc.ALARM_MAX_CHARS_PER_HOUR <= 10000
