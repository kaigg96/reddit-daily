# Asset credits & licenses

Every media asset committed to this repo must be listed here with its source and license
(PRD constraint 6: free for commercial use, no attribution required).

| Asset | Source | License |
|---|---|---|
| `fonts/Anton-Regular.ttf` | https://github.com/google/fonts/tree/main/ofl/anton | SIL Open Font License 1.1 (`fonts/OFL.txt`) |
| `sfx/whoosh_*.mp3` | Generated in-repo by `scripts/make_sfx.py` (synthesized noise sweeps) | Original work, no third-party material |
| `funk_bg_lower.mp3` | YouTube Audio Library (owner-confirmed 2026-07-18); volume-lowered copy | YouTube Audio Library license |
| `broll/pexels_7565434.mp4` | https://www.pexels.com/video/7565434/ | Pexels License |
| `broll/pexels_7565898.mp4` | https://www.pexels.com/video/7565898/ | Pexels License |
| `broll/pexels_9668945.mp4` | https://www.pexels.com/video/9668945/ | Pexels License |
| `broll/pexels_12488544.mp4` | https://www.pexels.com/video/12488544/ | Pexels License |
| `broll/pexels_15022349.mp4` | https://www.pexels.com/video/15022349/ | Pexels License |
| `broll_retired/pexels_15168364.mp4` | https://www.pexels.com/video/15168364/ | Pexels License — retired 2026-10-26: 6 of 21 uploads using it sat at ≤5 views (p=0.003 under the 0.0071 bar, PRD §0 #11) |
| `broll_retired/pexels_16482908.mp4` | https://www.pexels.com/video/16482908/ | Pexels License — retired 2026-09-28: 8 of 16 uploads using it sat at ≤5 views |
| `music/` | *(empty — optional: add more Audio Library tracks for variety)* | Record each track here |

## Services whose output is in the video — paid use (read 2026-10-18)

ORG.md's "before monetizing" check. None bars paid use; Reddit's terms (PLAN.md §4) still do.
Re-read before applying to any programme.

| Service | What it makes | Terms, quoted |
|---|---|---|
| Amazon Polly | narration | Polly FAQ: "As between you and AWS, your Polly output belongs to you"; replay "The service does not restrict this" |
| Gemini API (free tier) | titles, CTA, host lines, screen | Gemini API Additional Terms (modified 2026-04-28): "Google won't claim ownership over that content"; no clause bars commercial use of Unpaid Services. EEA/CH/UK: paid only when "making API Clients available to users" there; our client is not offered to anyone |
| Groq (fallback, `v8`) | the same, on Gemini failure | Groq Services Agreement (2026-06-22) §8.1: "Customer retains all Intellectual Property Rights in Customer Data (including in Inputs and Outputs)" |
| Pexels clips | backgrounds | Pexels License: free, commercial use allowed; "Identifiable people may not appear in a bad light". All five live clips are abstract (ink, smoke, fog, fire, a roof), checked one frame each: a new clip with people needs this read against dark topics. Redistribution (read 2026-10-30): it bars only "other stock photo or wallpaper platforms" and selling "unaltered copies"; this public repo's committed clips are neither |
