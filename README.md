# hs-ops

Configuración y backups de HealthSignals. Implementa la opción C de la política de backups: GitHub Actions exporta por API todos los días, sin depender de Make, de ningún servidor ni de la laptop.

## Qué se respalda (workflow `backup-daily`, 9:23 UTC)
- `make/scenarios/`: blueprint de cada escenario (secretos redactados; ver `make/redactions.json`).
- `make/data-store-records/`: registros de los data stores operativos (148747 dedup eventos, 161375 gate, 162492 reglas Voices, 164495 dedup social). Nunca 128118 (X OAuth).
- `make/data-stores.json`, `data-structures.json`, `hooks.json` (sin URL), `connections.json` (sin credenciales).
- `airtable/<base>/`: esquema y registros de cada tabla de las bases HealthSignals, HealthSignals Brief y Prospect Intelligence (sin URLs firmadas de adjuntos).
- `runbooks/`: cómo restaurar y recuperar cuentas; `runbooks/scheduled-tasks.md` con las tareas programadas de Claude.

## Controles
- El job falla (y no manda heartbeat) si exporta menos de 20 escenarios, 5 data stores o 5 tablas: un backup vacío no cuenta.
- gitleaks escanea `make/` y `airtable/` antes de cada commit; si encuentra algo, no se sube nada.
- Espejo diario en un segundo proveedor (`MIRROR_URL`) y heartbeat (`HEARTBEAT_URL`) que avisa por mail si pasan 26 h sin backup.

## Secretos del repo (Settings → Secrets and variables → Actions)
| Nombre | Qué es | Permisos |
|---|---|---|
| `MAKE_API_TOKEN` | Token de Make | scenarios:read, datastores:read, udts:read, hooks:read, connections:read |
| `AIRTABLE_TOKEN` | PAT de Airtable | data.records:read, schema.bases:read |
| `MIRROR_URL` | URL https con token del repo espejo | escritura solo en ese repo |
| `HEARTBEAT_URL` | URL de ping de healthchecks.io | — |

Todos rotan cada 90 días. Los valores viven en Bitwarden, nunca en el repo ni en chats.

## Reglas
- Commits del job: `backup:`. Cambios a mano: `change:`.
- Ningún blueprint entra al repo si no lo escribió `export_make.py` (un copy-paste manual saltea la redacción de secretos).
