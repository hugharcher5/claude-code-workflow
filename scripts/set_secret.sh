#!/usr/bin/env bash
# Safe secret installation (Feature 6).
# Prompts silently for a value and writes NAME=value into the CURRENT
# PROJECT's .env — never into this kit, never echoed, never logged.
#
# Usage: scripts/set_secret.sh VAR_NAME [path/to/.env]
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $(basename "$0") VAR_NAME [path/to/.env]" >&2
  exit 1
fi

VAR_NAME="$1"
ENV_FILE="${2:-.env}"

if [[ ! "$VAR_NAME" =~ ^[A-Za-z_][A-Za-z0-9_]*$ ]]; then
  echo "Not a valid env var name: $VAR_NAME" >&2
  exit 1
fi

# Refuse to run inside this kit — secrets belong to coding projects, not here.
if [[ -f "$(dirname "$0")/../CLAUDE.md" ]] && grep -q "^# Personal Claude Kit" "$(dirname "$0")/../CLAUDE.md" 2>/dev/null; then
  if [[ "$(cd "$(dirname "$ENV_FILE")" && pwd)" == "$(cd "$(dirname "$0")/.." && pwd)" ]]; then
    echo "Refusing: this kit does not store project secrets. Run this inside the target project instead." >&2
    exit 1
  fi
fi

printf 'Value for %s (input hidden, not echoed): ' "$VAR_NAME" >&2
read -r -s VALUE
echo >&2

if [[ -z "$VALUE" ]]; then
  echo "Empty value — nothing written." >&2
  exit 1
fi

touch "$ENV_FILE"
chmod 600 "$ENV_FILE"

if grep -q "^${VAR_NAME}=" "$ENV_FILE" 2>/dev/null; then
  TMP_FILE="$(mktemp)"
  awk -v var="$VAR_NAME" -v val="$VALUE" 'BEGIN{FS=OFS="="} $1==var{$0=var"="val} {print}' "$ENV_FILE" > "$TMP_FILE"
  mv "$TMP_FILE" "$ENV_FILE"
else
  printf '%s=%s\n' "$VAR_NAME" "$VALUE" >> "$ENV_FILE"
fi

unset VALUE

if [[ -d .git ]] && ! git check-ignore -q "$ENV_FILE" 2>/dev/null; then
  echo "WARNING: $ENV_FILE is not git-ignored. Add it to .gitignore before committing anything." >&2
fi

echo "Set ${VAR_NAME} in ${ENV_FILE}. Value was not printed, logged, or journaled." >&2
