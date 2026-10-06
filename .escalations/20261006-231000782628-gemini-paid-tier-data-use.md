---
title: Move Gemini to the paid tier (about $1–3 a month), so the Reddit posts we send it stop being used to train Google's models?
key: gemini-paid-tier-data-use
labels: needs-owner,guardrail
raised_at: 2026-10-06T23:10:00+00:00
---

## What I found

Every upload sends Reddit posts and their comments to Gemini, which screens them and writes the title. We use Gemini's **free** allowance. Google's own pages, read first-hand tonight, say what that means:

- **Gemini's terms:** on the free allowance, "Google uses the content you submit to the Services and any generated responses to provide, improve, and develop Google products and services and machine learning technologies", and people at Google may read it.
- **Gemini's price page:** the row "Used to improve our products" reads **Yes** for the free tier and **No** for the paid tier, for the model we use.

**Reddit's Data API Terms (§3.2)** say we "must not, and must not allow those acting on your behalf to" use Reddit's content "to train a machine learning or AI model without the express permission of rightsholders". Reddit's Developer Terms say the same about training "large language, artificial intelligence, or other algorithmic models". Handing Reddit's posts to a service that says it uses them to improve its models sits badly with that. I am not a lawyer, and "on your behalf" can be argued. But this is the clause Reddit is known to enforce, and a request to Reddit (#60) invites exactly this question.

This is a new reason. When you declined the paid tier on 24 September (#22), the question was only the daily cap.

## What it would cost

The model we use costs $0.30 per million tokens in and $2.50 per million out, thinking included (Google's price page, tonight). Production makes 4 to 10 requests a day. At a few thousand tokens each way that is **about $1–3 a month**. If the daily release check and sample runs also move, the ceiling is about $5, at 20 requests a day with generous sizes. These are estimates; we do not log token counts.

## The control

This is new spend, so it needs a control at the provider as well as your approval. In Google Cloud, cap the Gemini API's requests per day for the project, for example at 40 (twice today's cap), and add a budget alert at $5 a month. No code changes: the same key starts billing once the project has billing.

## What else it buys

The 20-a-day cap has cost real uploads their titles and blocks the topic ranker, the top-ranked product experiment (#22). The paid tier removes both problems.

## If you say no

Nothing changes in production. #60 should then tell Reddit plainly how we use Gemini, rather than leave it for them to find.

## Recommendation

Yes: turn on billing for the Gemini project with a daily request cap set at Google, before anyone writes to Reddit (#60). It closes a breach of Reddit's terms we are in today, costs about $1–3 a month, and also lifts the 20-a-day cap that blocks the topic ranker.

---

*Raised automatically by a `/shift` run — it could not make this call itself. Close this issue once decided; if the decision changes a standing rule, it belongs in `CLAUDE.md` too.*