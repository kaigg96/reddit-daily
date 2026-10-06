---
title: Account security: the quarterly check has never run (six checks, about 15 minutes)
key: account-security-quarterly
labels: needs-owner
raised_at: 2026-10-06T17:21:57+00:00
---

## Why this is here

The company's plan lists one risk as fatal: losing the YouTube channel or the Google account that owns it. Its only answer is a quarterly account-security check, and that has never been held. The checks need your logins, so they are yours. What a shift can see, it has checked (below).

## Already checked by the shift (6 October)

- The repository's only collaborator is your account.
- No credentials are in the repository, and the secret files are still excluded.
- The Amazon key can only synthesize speech, and the spending cap and its automatic block are in place ($0.19 spent this month).

## The six checks (yours)

1. **Google account:** 2-step verification is on, ideally with a passkey or security key, not SMS alone. The recovery email and phone are current.
2. **YouTube channel:** in Studio's Settings, under Permissions, only people you expect have access. Consider a second owner you control, so one lost login is not the end of the channel.
3. **Third-party access** (Google Account → Security → "Your connections to third-party apps & services"): only our own uploader app holds YouTube access. Remove anything you do not recognise.
4. **GitHub:** 2-factor authentication is on. Under the repository's Settings, check for no unexpected deploy keys or webhooks. A shift is refused permission to see these.
5. **Amazon root account:** multi-factor sign-in is on. The spending checks cover the speech key, not the root login.
6. **Gemini API key:** restricted to the Generative Language API in Google Cloud's credentials page, so a leaked key cannot be used for anything else.

## What happens next

Reply with the date and any check that failed. A shift will record the date, so the next check comes due in January.

## Recommendation

Do the six checks below this week and reply with any that fail; checks 1 and 3 matter most, because losing the Google account loses the channel and everything on it.

---

*Raised automatically by a `/shift` run — it could not make this call itself. Close this issue once decided; if the decision changes a standing rule, it belongs in `CLAUDE.md` too.*