# hs-ops

Configuración y backups de HealthSignals. Implementa la opción C de la política de backups: GitHub Actions exporta por API, sin depender de Make ni de hs-cloud-01.

## Estructura
- `make/`: blueprints de escenarios, metadatos de data stores (sin records), estructuras, webhooks (sin URL) y conexiones (solo metadatos). Lo genera `backup-daily`.
- `airtable/`, `wordpress/`, `dns/`, `claude/`, `server/`, `runbooks/`: pendientes.
- `scripts/`: los exportadores.

## Reglas
- Commits del job: `backup:`. Cambios a mano: `change:`.
- Nada de secretos en git. El exportador redacta los patrones conocidos y anota dónde en `make/redactions.json`; el valor real está en Bitwarden.
- Secretos del repo (Settings → Secrets and variables → Actions): `MAKE_API_TOKEN` (solo lectura) y `HEARTBEAT_URL` (monitor que avisa si no hay backup en 26 h).

## Restaurar un escenario de Make
Tomá `make/scenarios/<id>-*.json` del último commit sano, subí el campo `blueprint` con `scenarios_update` y reponé desde Bitwarden lo que figure en `redactions.json`.
