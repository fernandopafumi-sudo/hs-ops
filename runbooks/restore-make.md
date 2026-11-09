# Restaurar un escenario de Make

Cuándo: un escenario se rompió por una edición, se borró, o quedó inválido.

## Si el escenario todavía existe (edición rota)
1. En hs-ops, buscar el último commit sano: `git log --oneline -- make/scenarios/<ID>-*.json`.
2. Tomar ese archivo y subir su campo `blueprint` con `scenarios_update` (MCP de Make), en el mismo ID. Mantiene ID, webhook y nombre de la herramienta MCP.
3. Reponer a mano lo que figure en `make/redactions.json` para ese ID (los valores están en Bitwarden).
4. Correr una vez con una fila de prueba y mirar la ejecución.

## Si el escenario fue borrado
1. Recuperar el JSON del historial: `git log --diff-filter=D --name-only -- make/scenarios/` y `git show <commit>^:make/scenarios/<archivo>`.
2. Crear uno nuevo con `scenarios_create` (team 2174293) usando `blueprint` y `scheduling`. **Tiene otro ID.**
3. Reponer secretos redactados (Bitwarden).
4. Actualizar todo lo que citaba el ID viejo: ver `runbooks/scheduled-tasks.md` (prompts de tareas), skills (`hs-*`, `make-scenario-deploy`), notas de Airtable, otros escenarios que lo llamen. El nombre de la herramienta MCP cambia (`s<ID>_...`).
5. Si tenía webhook, el hook nuevo tiene otra URL: actualizarla donde se use (sitio, formularios, apps OAuth).
6. Activar y verificar `nextExec`.

## Simulacro (hacer una vez por trimestre)
Escenario de prueba: 6234149 (Brief Render Test, on-demand, sin dependencias). Borrarlo, recrearlo con los pasos de arriba, cronometrar y anotar acá la fecha y el tiempo.

| Fecha | Escenario | Tiempo | Notas |
|---|---|---|---|
| | | | |
