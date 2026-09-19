"""Gemini calls. Every function fails soft: the video must ship without them."""

import os
import re

import requests

from . import config  # noqa: F401  (ensures .env is loaded for direct imports)


# gemini-2.5-flash "thinks" by default, and on these prompts that is pure
# latency: measured 2026-09-19, one title call spent 546 reasoning tokens to
# emit an 8-token title and took 33.1s — past the 30s timeout this module used
# to use, so the call raised ReadTimeout and the run shipped the raw Reddit
# question instead of a generated title. Disabling thinking put the same call
# at 0.6s. Every task here (keyword extraction, title rephrasing, a one-line
# CTA, the R4.6 screen's JSON verdict) is a short transformation, not a
# reasoning problem.
#
# thinkingConfig requires v1beta: v1 rejects it with "Thinking is not enabled
# for api version v1." That is the only reason this module is on v1beta.
_ENDPOINT = ("https://generativelanguage.googleapis.com/v1beta/models/"
             "gemini-2.5-flash:generateContent")

# Generous because it is now only a backstop against a pathological response,
# not a routine limit — with thinking off, calls land in about a second.
# requests' timeout is per-read, not a total deadline, so this does not bound
# total call duration; it only stops a stalled socket hanging the run.
_TIMEOUT = 60


def _generate(prompt, thinking_budget=0):
    """One Gemini call. `thinking_budget=0` disables reasoning tokens (the
    default, and what every caller here wants); pass a token budget only for a
    task where reasoning demonstrably helps."""
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"thinkingConfig": {"thinkingBudget": thinking_budget}},
    }
    resp = requests.post(
        f"{_ENDPOINT}?key={os.environ['GEMINI_API_KEY']}",
        headers={"Content-Type": "application/json"},
        json=body,
        timeout=_TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()["candidates"][0]["content"]["parts"][0]["text"]


def get_keywords(reddit_title, comments):
    prompt = f"""
I'm publishing a YouTube video answering the following question: {reddit_title}.

Here are the responses I'll be highlighting: {comments[0]}, {comments[1]}, {comments[2]}.

Please extract the 10 best topics or keywords I can add to the video to maximize search optimization and virality.
Include a mix of short-tail and long-tail keywords that people searching for answers to this question or related discussions might use. Also, consider terms related to the themes in the provided comments.

Do not include any context or explanations, return only the 10 keywords numbered in the following format:
```
    1. keyword1
    2. keyword2
    ...
    10.keyword10
```
"""
    try:
        return re.findall(r"\d+\.\s*(.*)", _generate(prompt))
    except Exception as e:
        # never echo the exception body: HTTPError messages embed the keyed URL
        print(f"Gemini keywords failed with {type(e).__name__} (continuing without)")
        return []


# PRD R2.2: three title-style experiments, rotated deterministically per day
# and logged per upload so performance is comparable offline.
_STYLE_GUIDANCE = {
    "A": """
- Be a captivating and concise rephrasing or transformation of the original Reddit question: "{reddit_title}".
- Spark strong curiosity and make viewers eager to see the answers.""",
    "B": """
- Address the viewer directly in the second person ("You...", "Which one are you?", "You'll wish you knew this...").
- Make it feel like a personal question or challenge aimed at the viewer, derived from the original Reddit question: "{reddit_title}".""",
    "C": """
- Lead with the number of answers, list-style (e.g. "3 Answers That...", "3 People Reveal...").
- Frame the video as a countable list distilled from the original Reddit question: "{reddit_title}".""",
}


def get_video_title(reddit_title, comments, style="A"):
    guidance = _STYLE_GUIDANCE.get(style, _STYLE_GUIDANCE["A"]).format(reddit_title=reddit_title)
    prompt = f"""
I'm creating a YouTube Short video based on the Reddit question: "{reddit_title}".
The video will feature these key answers from the comments:
1. "{comments[0]}"
2. "{comments[1]}"
3. "{comments[2]}"

Your goal is to craft a highly engaging YouTube video title that maximizes click-through rate (CTR) and encourages virality.

The title should:{guidance}
- Use impactful and engaging language.
- Be suitable for a YouTube Short (generally under 70 characters is good, but impact is key).
- Hint at the nature of the answers/discussion without giving away specifics from the comments.
- NOT be overly clickbaity or sensational.

Important: Return *only* the generated title. Do not include any surrounding quotes, introductory phrases like "Here's a title:", or any other explanatory text. Just the title itself.
"""
    try:
        return _generate(prompt)
    except Exception as e:
        print(f"Gemini title failed with {type(e).__name__} (falling back to reddit title)")
        return None


def get_cta(reddit_title):
    """R3.1a: a ≤12-word question-specific spoken outro. None → caller uses the
    generic fallback. Fails soft."""
    prompt = f"""
My YouTube Short asks: "{reddit_title}" and shows the top three Reddit answers.

Write a spoken outro line of AT MOST 12 words asking viewers to comment their
own answer to this specific question. Direct, punchy, conversational.
No hashtags, no emojis, no profanity.

Return only the line itself — no quotes, no explanation.
"""
    try:
        line = re.sub(r"[*_`]", "", _generate(prompt))  # strip markdown emphasis
        return re.sub(r"\s+", " ", line).strip().strip('"').strip("'").strip() or None
    except Exception as e:
        print(f"Gemini CTA failed with {type(e).__name__} (using generic outro)")
        return None


def sanitize_title(title, fallback, max_len=100):
    """Strip LLM artifacts (R0.5). 100 is YouTube's title limit."""
    if not title:
        return fallback[:max_len]
    title = re.sub(r"\s+", " ", title).strip().strip('"').strip("'").strip()
    if not title:
        return fallback[:max_len]
    return title[:max_len]
