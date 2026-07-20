"""Gemini calls. Every function fails soft: the video must ship without them."""

import os
import re

import requests


def _generate(prompt):
    endpoint = (
        "https://generativelanguage.googleapis.com/v1/models/"
        f"gemini-2.5-flash:generateContent?key={os.environ['GEMINI_API_KEY']}"
    )
    resp = requests.post(
        endpoint,
        headers={"Content-Type": "application/json"},
        json={"contents": [{"parts": [{"text": prompt}]}]},
        timeout=30,
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


def get_video_title(reddit_title, comments):
    """Title style A: curiosity rephrase (PRD R2.2 adds B/C variants later)."""
    prompt = f"""
I'm creating a YouTube Short video based on the Reddit question: "{reddit_title}".
The video will feature these key answers from the comments:
1. "{comments[0]}"
2. "{comments[1]}"
3. "{comments[2]}"

Your goal is to craft a highly engaging YouTube video title that maximizes click-through rate (CTR) and encourages virality.

The title should:
- Be a captivating and concise rephrasing or transformation of the original Reddit question: "{reddit_title}".
- Spark strong curiosity and make viewers eager to see the answers.
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


def sanitize_title(title, fallback, max_len=84):
    """Strip LLM artifacts (R0.5). max_len leaves room for the 16-char hashtag suffix."""
    if not title:
        return fallback[:max_len]
    title = re.sub(r"\s+", " ", title).strip().strip('"').strip("'").strip()
    if not title:
        return fallback[:max_len]
    return title[:max_len]
