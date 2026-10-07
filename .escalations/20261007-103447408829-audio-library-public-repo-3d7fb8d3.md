---
title: Our public project shares the background music, which YouTube's Audio Library terms forbid. A two-minute fix is ready
key: audio-library-public-repo-3d7fb8d3
labels: needs-owner,security
raised_at: 2026-10-07T10:34:47+00:00
---

## What I found

Since the project went public on 5 October, anyone can download the background music from it: the one YouTube Audio Library track every upload uses. The Audio Library's terms, as quoted by several guides (the terms themselves sit behind YouTube Studio's login, where you can confirm them), say: *"You may not make available, distribute or perform the music files from this library separately from videos and other content into which you have incorporated these music files (e.g., standalone distribution of these files is not permitted)."*

The likelihood of anyone acting on it is low, but it is a breach of YouTube's terms by the channel YouTube would pay. The fix is cheap. The stock video clips are fine: Pexels' licence bars only stock and wallpaper sites and selling unaltered copies.

## The fix, ready for you

1. **Label this issue `approved`.** That applies the patch below: the video job (and the sample-video job) decrypts the music just before rendering. Until step 2 it does nothing.
2. **Then, on your machine:** pull the project, then `scripts/seal_assets.sh`, then `git push origin main`. It makes a random key and saves it as the secret `ASSET_KEY`, replaces the plain track with an encrypted copy, checks the copy decrypts exactly, and commits. About two minutes. It refuses to run before step 1 is in.

If the key ever goes missing, an upload goes out without music rather than failing, and the upload log's music column says "none", which the next shift's first check reads.

**Two things the fix does not do.** Old versions of the project still hold the plain file. Erasing it from history means rewriting every past version, which is disruptive and doesn't reach copies already taken. I would not, unless someone asks. And please do not add more Audio Library tracks for variety until the seal is in; the script seals those too.

## The exact change

Applied automatically, exactly as shown, when you label this `approved`.

<!-- apply-patch -->
`````diff
diff --git a/.github/workflows/dry-run.yml b/.github/workflows/dry-run.yml
index f8c7682..b78f321 100644
--- a/.github/workflows/dry-run.yml
+++ b/.github/workflows/dry-run.yml
@@ -97,6 +97,20 @@ jobs:
           ref: ${{ steps.req.outputs.branch }}
           path: under-test
 
+      # As in the video job: the music is sealed because the repo is public.
+      # Its own step, before the branch's dependencies are installed and with the
+      # system openssl, so nothing the branch brings can see the key.
+      - name: Unseal licensed music
+        if: steps.req.outputs.go == 'true'
+        working-directory: under-test
+        env:
+          ASSET_KEY: ${{ secrets.ASSET_KEY }}
+        run: |
+          git ls-files -z 'assets/*.enc' | while IFS= read -r -d '' f; do
+            /usr/bin/openssl enc -d -aes-256-cbc -pbkdf2 -in "$f" -out "${f%.enc}" -pass env:ASSET_KEY \
+              || { rm -f "${f%.enc}"; echo "::warning::could not unseal $f; the sample renders without it"; }
+          done
+
       - uses: actions/setup-python@v5
         if: steps.req.outputs.go == 'true'
         with:
diff --git a/.github/workflows/run-reddit-video.yml b/.github/workflows/run-reddit-video.yml
index 8f1a3e3..f8a7db3 100644
--- a/.github/workflows/run-reddit-video.yml
+++ b/.github/workflows/run-reddit-video.yml
@@ -38,6 +38,20 @@ jobs:
         python -m pip install --upgrade pip
         pip install -r requirements.txt
 
+    # YouTube Audio Library terms bar making the music files available apart
+    # from videos, and this repo is public, so it carries them encrypted
+    # (scripts/seal_assets.sh). A track that fails to unseal is removed rather
+    # than left as noise; the video then renders without it, and upload_log's
+    # music_track column records "none".
+    - name: Unseal licensed music
+      env:
+        ASSET_KEY: ${{ secrets.ASSET_KEY }}
+      run: |
+        git ls-files -z 'assets/*.enc' | while IFS= read -r -d '' f; do
+          /usr/bin/openssl enc -d -aes-256-cbc -pbkdf2 -in "$f" -out "${f%.enc}" -pass env:ASSET_KEY \
+            || { rm -f "${f%.enc}"; echo "::warning::could not unseal $f; the video renders without it"; }
+        done
+
     - name: Generate video (and upload unless dry run)
       env:
         REDDIT_CLIENT_ID: ${{ secrets.REDDIT_CLIENT_ID }}
`````
patch-sha256: 3d7fb8d3cc4db4130457a736b354e7439eb86ba38d8e7055d3f526e95d8a317d

## Recommendation

Approve: label this issue, then run scripts/seal_assets.sh once on your machine and push. Leave the old history as it is unless someone asks; rewriting it is disruptive and does not reach copies already taken.

---

*Raised automatically by a `/shift` run — it could not make this call itself. Close this issue once decided; if the decision changes a standing rule, it belongs in `CLAUDE.md` too.*