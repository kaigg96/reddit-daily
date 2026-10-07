#!/usr/bin/env bash
# Seal the YouTube Audio Library music so the public repo stops distributing it.
#
# The Audio Library terms say "You may not make available, distribute or
# perform the music files from this library separately from videos", and this
# repo has been public since 2026-10-05 (TECH_DEBT.md). After this runs, the
# repo carries each track encrypted, the key lives only in the ASSET_KEY
# Actions secret, and the workflows unseal it just before rendering.
#
# The owner's, run once from the repo root on an up-to-date main, and only
# AFTER the workflow patch that unseals the files has been applied. Otherwise
# the next upload renders without music. It needs `gh` logged in with admin on
# the repo (to set the secret) and an `openssl` that supports -pbkdf2.
#
# Run it once. The key is never written anywhere but the secret, so sealing
# again would orphan the files already sealed; the script refuses.
#
# Git history keeps the plain file; rewriting history is a separate decision.
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"
grep -q 'ASSET_KEY' .github/workflows/run-reddit-video.yml \
  || { echo "Apply the workflow patch first: the video job does not unseal yet." >&2; exit 1; }
[ -z "$(git ls-files 'assets/*.enc')" ] \
  || { echo "Already sealed. A new key would orphan the sealed files; nothing changed." >&2; exit 1; }

plain=()
for f in assets/funk_bg_lower.mp3 assets/music/*.mp3; do
  [ -f "$f" ] && plain+=("$f")
done
[ "${#plain[@]}" -gt 0 ] || { echo "No plain tracks found; nothing changed." >&2; exit 1; }

# Encrypt and prove each round trip before git or the secret changes.
KEY="$(openssl rand -base64 32)"
export KEY
for f in "${plain[@]}"; do
  openssl enc -aes-256-cbc -pbkdf2 -salt -in "$f" -out "$f.enc" -pass env:KEY \
    || { echo "openssl could not encrypt $f; nothing changed in git or the secret." >&2; exit 1; }
  openssl enc -d -aes-256-cbc -pbkdf2 -in "$f.enc" -pass env:KEY | cmp -s - "$f" \
    || { echo "Round trip failed for $f; nothing changed in git or the secret." >&2; exit 1; }
done

gh secret set ASSET_KEY --body "$KEY"

for f in "${plain[@]}"; do
  git rm --cached -q "$f"
  git add "$f.enc"
done
for pattern in '/assets/funk_bg_lower.mp3' '/assets/music/*.mp3'; do
  grep -qxF "$pattern" .gitignore || echo "$pattern" >> .gitignore
done
git add .gitignore
git commit -q -m "Seal the Audio Library music: encrypted in the repo, unsealed in CI"
echo "Sealed ${#plain[@]} track(s). Your local plain copies stay for local renders."
echo "Push with: git push origin main"
