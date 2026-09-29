#!/usr/bin/env python3
"""Get a branch rendered without holding the keys to render it.

A shift cannot render a video. It holds no Polly or Reddit credentials,
deliberately, and it cannot start a workflow either: the Claude action swaps
the workflow token for its own, which has no Actions permission (#27). So it
asks, and `.github/workflows/dry-run.yml` renders:

    dry_run.py request <branch>   # queue it, then commit and push the file
    dry_run.py pending            # (dry-run.yml) which branch to render
    dry_run.py check <video.mp4>  # (dry-run.yml) is this a playable video?
    dry_run.py record ...         # (dry-run.yml) write the verdict

The render job holds no YouTube credentials, so nothing it runs can publish.
The verdict lands in .github/last-dry-run.md. Merge only on a PASS that names
the branch's current commit.
"""
import argparse
import contextlib
import datetime
import glob
import io
import os
import re
import subprocess
import sys

QUEUE = ".dry-run-requests"
VERDICT = ".github/last-dry-run.md"
BRANCH_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._/-]{0,99}")

# What a render must be. Calibrated 2026-09-24 against a render that shipped:
# 18.8 s long, with one natural 0.34 s pause after the title. PRD §9's older
# "20-40 s, no silence >= 0.3 s" would have failed it -- 25 of the last 60
# uploads ran under 20 s. This gate exists to catch a BROKEN render, not to
# judge the format, so the bounds are wide.
SIZE = (1080, 1920)
FPS = (29.5, 30.5)
DURATION = (10.0, 59.0)
DEAD_AIR_S = 1.0


def valid_branch(name):
    return bool(name) and BRANCH_RE.fullmatch(name) is not None and ".." not in name


def request(branch):
    if not valid_branch(branch):
        sys.exit(f"not a branch name this will render: {branch!r}")
    if subprocess.run(["git", "ls-remote", "--exit-code", "--heads", "origin", branch],
                      capture_output=True).returncode != 0:
        sys.exit(f"{branch} is not on origin -- push it first")
    os.makedirs(QUEUE, exist_ok=True)
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    path = os.path.join(QUEUE, branch.replace("/", "--") + ".md")
    with open(path, "w") as f:
        f.write(f"branch: {branch}\nrequested_at: {now}\n")
    print(f"queued {path}\ncommit and push it -- dry-run.yml renders it and writes "
          f"{VERDICT} (5-10 minutes; at most one automated render per 12 hours)")
    return 0


def pending(queue=QUEUE):
    """The most recently requested valid branch, or nothing."""
    found = []
    for path in glob.glob(os.path.join(queue, "*.md")):
        if os.path.basename(path) == "README.md":
            continue
        fields = dict(line.split(":", 1) for line in open(path).read().splitlines()
                      if ":" in line)
        branch = fields.get("branch", "").strip()
        if valid_branch(branch):
            found.append((fields.get("requested_at", "").strip(), branch))
    if found:
        print(max(found)[1])
    return 0


def judge(size, fps, duration, has_audio, frames_ok, decode_errors, silences):
    """Pure verdict over measured facts: (ok, [reasons it failed])."""
    bad = []
    if tuple(size) != SIZE:
        bad.append(f"size {size[0]}x{size[1]}, expected {SIZE[0]}x{SIZE[1]}")
    if not FPS[0] <= fps <= FPS[1]:
        bad.append(f"{fps:g} fps, expected 30")
    if not DURATION[0] <= duration <= DURATION[1]:
        bad.append(f"{duration:.1f} s long, outside {DURATION[0]:g}-{DURATION[1]:g} s")
    if not has_audio:
        bad.append("no audio track")
    if not frames_ok:
        bad.append("frames could not be decoded")
    if decode_errors:
        bad.append("decoder errors: " + decode_errors[:200])
    long_gaps = [s for s in silences if s[1] >= DEAD_AIR_S]
    if long_gaps:
        bad.append("dead air: " + ", ".join(f"{d:.1f} s at {t:.1f} s" for t, d in long_gaps))
    return not bad, bad


def check(path):
    if not os.path.exists(path):
        print("FAIL -- the render produced no video")
        return 1
    import imageio_ffmpeg
    from moviepy import VideoFileClip
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    with contextlib.redirect_stdout(io.StringIO()):   # moviepy prints probe dicts
        clip = VideoFileClip(path)
        size, fps, duration = clip.size, clip.fps, clip.duration
        has_audio = clip.audio is not None
        try:
            for t in (0.5, duration / 2, max(duration - 0.5, 0)):
                clip.get_frame(t)
            frames_ok = True
        except Exception:
            frames_ok = False
        clip.close()
    decode = subprocess.run([ff, "-v", "error", "-i", path, "-f", "null", "-"],
                            capture_output=True, text=True).stderr.strip()
    err = subprocess.run([ff, "-hide_banner", "-i", path, "-af",
                          f"silencedetect=n=-35dB:d={DEAD_AIR_S}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    silences = [(float(t), float(d)) for t, d in zip(
        re.findall(r"silence_start: ([\d.]+)", err),
        re.findall(r"silence_duration: ([\d.]+)", err))]
    ok, bad = judge(size, fps, duration, has_audio, frames_ok, decode, silences)
    if ok:
        print(f"PASS -- playable: {size[0]}x{size[1]}, {fps:g} fps, {duration:.1f} s, "
              f"audio, no dead air")
        return 0
    print("FAIL -- " + "; ".join(bad))
    return 1


HEAD = """# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.
"""


SOFT_FAILURE = re.compile(r"failed|not logged|not collected|fall(?:ing)? ?back", re.I)
# What the run chose, and what the screen turned down on the way. A new
# subreddit needs its screen replayed before it ships (PRD §6 R4.1), and the
# log that shows the replay is otherwise readable only in Actions.
PICKED = re.compile(r"^(Selected post:|Screen:|Slate topics|Title style|Today's top )")


def record(args):
    """Rewrite the verdict file. A refusal leaves the last render intact."""
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    old = open(VERDICT).read() if os.path.exists(VERDICT) else ""
    last_render = old.split("## Last render", 1)[1].split("## Last request", 1)[0] \
        if "## Last render" in old else "\n_None yet._\n\n"
    if args.refused:
        outcome = f"not rendered -- {args.refused}"
    else:
        check_line = (open(args.check_file).read().strip()
                      if args.check_file and os.path.exists(args.check_file) else "")
        passed = args.render_code == 0 and check_line.startswith("PASS")
        if passed:
            verdict = "✅ " + check_line
        elif args.render_code != 0:
            verdict = f"❌ FAIL -- the pipeline exited {args.render_code}"
        else:
            verdict = "❌ " + (check_line or "FAIL -- the render could not be checked")
        body = [f"- **Branch:** `{args.branch}`", f"- **Commit:** `{args.commit}`",
                f"- **When:** {now}", f"- **Verdict:** {verdict}", "",
                f"[Sample video and full output]({args.run_url})"]
        if passed and args.log and os.path.exists(args.log):
            # A PASS only proves the video plays. A Gemini call that failed soft
            # (raw title, no slate) says so only in the log, which shifts cannot read.
            soft = [l for l in open(args.log, errors="replace").read().splitlines()
                    if SOFT_FAILURE.search(l)][:10]
            if soft:
                body += ["", "Failed soft (the video still passed):", "", "```", *soft, "```"]
            picked = [l for l in open(args.log, errors="replace").read().splitlines()
                      if PICKED.match(l)][:12]
            if picked:
                body += ["", "What it picked:", "", "```", *picked, "```"]
        if not passed and args.log and os.path.exists(args.log):
            tail = open(args.log, errors="replace").read().splitlines()[-40:]
            body += ["", "<details><summary>Last 40 lines of the run "
                     "(secrets redacted)</summary>", "", "```",
                     "\n".join(tail)[-4000:], "```", "", "</details>"]
        last_render = "\n" + "\n".join(body) + "\n\n"
        outcome = "rendered -- see above"
    request_block = f"\n- **Branch:** `{args.branch or '?'}`\n- **When:** {now}\n" \
                    f"- **Outcome:** {outcome}\n"
    os.makedirs(os.path.dirname(VERDICT), exist_ok=True)
    with open(VERDICT, "w") as f:
        f.write(HEAD + "\n## Last render\n" + last_render + "## Last request\n"
                + request_block)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("request").add_argument("branch")
    sub.add_parser("pending")
    sub.add_parser("check").add_argument("video")
    r = sub.add_parser("record")
    r.add_argument("--branch", default="")
    r.add_argument("--commit", default="")
    r.add_argument("--render-code", type=int, default=1)
    r.add_argument("--check-file")
    r.add_argument("--log")
    r.add_argument("--run-url", default="")
    r.add_argument("--refused")
    a = ap.parse_args(argv)
    if a.cmd == "request":
        return request(a.branch)
    if a.cmd == "pending":
        return pending()
    if a.cmd == "check":
        return check(a.video)
    return record(a)


if __name__ == "__main__":
    sys.exit(main())
