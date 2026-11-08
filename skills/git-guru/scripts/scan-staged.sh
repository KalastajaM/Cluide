#!/usr/bin/env bash
# Baseline scan of the ADDED lines in the staged diff for secrets and personal data.
# Reports file:line and a label only; never prints the matched value.
# Usage: scan-staged.sh [--extra <pattern-file>]   (one extended regex per line,
#        e.g. internal project names; lines starting with # are skipped)
# Exit: 0 clean, 1 findings, 2 could not scan (fails closed).
set -uo pipefail
extra=""
if [ "${1:-}" = "--extra" ]; then extra=${2:?pattern file missing}; [ -r "$extra" ] || { echo "cannot read $extra" >&2; exit 2; }; fi
git rev-parse --git-dir >/dev/null 2>&1 || { echo "not a git repository" >&2; exit 2; }
diff=$(git --no-pager diff --cached -U0 --no-color --no-ext-diff) || { echo "git diff --cached failed" >&2; exit 2; }
names=$(git --no-pager diff --cached --name-only --diff-filter=AM) || { echo "git diff --name-only failed" >&2; exit 2; }
[ -z "$names" ] && { echo "nothing staged"; exit 0; }

added=$(printf '%s\n' "$diff" | awk '
  /^\+\+\+ / { f=$2; sub(/^b\//,"",f); next }
  /^@@ / { split($3,a,","); n=substr(a[1],2)+0; next }
  /^\+/ { print f ":" n ":" substr($0,2); n++ }')

hits=0
report(){ printf 'FINDING  %s  %s\n' "$1" "$2"; hits=$((hits+1)); }
check(){ # label regex [grep-flags] [exclude-regex]
  local label=$1 re=$2 flags=${3:-} skip=${4:-}
  while IFS= read -r m; do
    [ -n "$skip" ] && grep -qiE -- "$skip" <<<"$m" && ! grep -E $flags -- "$re" <<<"$(sed -E "s#$skip##g" <<<"$m")" >/dev/null && continue
    report "${m%%:*}:$(cut -d: -f2 <<<"$m")" "$label"
  done < <(printf '%s\n' "$added" | grep -E $flags -- "^[^:]*:[0-9]+:.*($re)" || true)
}
check "private key block"         'BEGIN [A-Z ]*PRIVATE KEY'
check "AWS access key id"         'AKIA[0-9A-Z]{16}'
check "GitHub token"              '(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}'
check "Slack token"               'xox[abprs]-[A-Za-z0-9-]{10,}'
check "Google API key"            'AIza[0-9A-Za-z_-]{35}'
check "Anthropic/OpenAI key"      'sk-(ant-)?[A-Za-z0-9_-]{20,}'
check "credential assignment"     '(api[_-]?key|secret|token|passw(or)?d|client[_-]?secret)["'"'"']?[[:space:]]*[:=][[:space:]]*["'"'"'][^"'"'"'[:space:]]{8,}' -i
check "connection string w/ pass" '[a-z]+://[^/[:space:]:@]+:[^/[:space:]@]+@'
check "home path with username"   '/(Users|home)/[a-z][a-z0-9._-]+/' -i '/(Users|home)/(you|your-?name|user|username|name|me|example|runner)/'
check "IBAN"                      '\b[A-Z]{2}[0-9]{2}[[:space:]]?([A-Z0-9]{4}[[:space:]]?){3,7}[A-Z0-9]{1,4}\b'
if [ -n "$extra" ]; then
  while IFS= read -r re; do case "$re" in ''|\#*) continue;; esac; check "extra: $re" "$re" -i; done < "$extra"
fi
while IFS= read -r f; do
  case "$(basename "$f")" in
    .env|.env.*|*.pem|*.key|*.p12|*.pfx|id_rsa|id_ed25519|credentials.json|*.keystore) report "$f" "sensitive file type staged";;
  esac
done <<<"$names"

if [ "$hits" -gt 0 ]; then
  echo "$hits finding(s): show each to the user and wait." >&2
  exit 1
fi
echo "clean: no baseline pattern matched the staged additions (read the diff too)"
