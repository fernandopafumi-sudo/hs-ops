# hs-ops

Backups cifrados de HealthSignals.

- `scripts/backup.sh`: corre en hs-cloud-01 vía cron, zipea, cifra con age y sube a `backups/`. Retención 30 días.
- `scripts/hs-ops-backup.cron`: copiar a `/etc/cron.d/hs-ops-backup`.
- `.github/workflows/backup-check.yml`: verifica a diario que exista el backup del día; si falta, falla y GitHub avisa por mail.

Restaurar: `age -d -i clave.txt -o backup.zip backups/hs-ops-backup-AAAA-MM-DD.zip.age` (clave privada en Bitwarden).
