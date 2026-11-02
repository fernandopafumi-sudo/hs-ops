#!/usr/bin/env bash
# Backup diario HealthSignals -> repo privado hs-ops (cifrado con age)
# Corre en hs-cloud-01 vía cron. Requiere: zip, age, git, clave deploy SSH con write al repo.
set -euo pipefail

# --- CONFIG (completar) ---
SRC_PATHS=(/srv/hs-ops)                  # SUPUESTO: carpetas a respaldar; ajustar a la política
AGE_RECIPIENT="age1REEMPLAZAR"           # clave pública age; la privada va a Bitwarden
REPO_DIR=/opt/hs-ops-repo                # clon local de git@github.com:fernandopafumi-sudo/hs-ops.git
KEEP_DAYS=30
# ---------------------------

DATE=$(date -u +%F)
NAME="hs-ops-backup-${DATE}.zip"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

zip -qr "$TMP/$NAME" "${SRC_PATHS[@]}"
age -r "$AGE_RECIPIENT" -o "$TMP/$NAME.age" "$TMP/$NAME"
sha256sum "$TMP/$NAME" | awk '{print $1}' > "$TMP/$NAME.sha256"

cd "$REPO_DIR"
git pull -q --rebase
mkdir -p backups
mv "$TMP/$NAME.age" "$TMP/$NAME.sha256" backups/

# retención: borra cifrados de más de KEEP_DAYS días
find backups -name 'hs-ops-backup-*.zip.age' -mtime +"$KEEP_DAYS" -print0 | while IFS= read -r -d '' f; do
  git rm -q "$f" "${f%.age}.sha256" 2>/dev/null || true
done

git add backups
git -c user.name="hs-cloud-01" -c user.email="ops@healthsignals.news" commit -qm "backup ${DATE}"
git push -q
