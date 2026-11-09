# Perdí la cuenta o el team de Make

Objetivo: volver a publicar en 6 h (RTO de la política).

Orden (cada paso depende del anterior):
1. Team nuevo en Make (zona us2). Anotar el nuevo teamId.
2. Conexiones: recrearlas con las credenciales de Bitwarden (Google editor@, Airtable PAT "Make - HealthSignals", WordPress, Anthropic, OpenAI, Exa, Brevo, Resend, LinkedIn page, Google Search Console). La lista de qué existía está en `make/connections.json`.
3. Data structures: recrear desde `make/data-structures.json`.
4. Data stores: crearlos con esas estructuras y cargar registros desde `make/data-store-records/`. 128118 (X OAuth) se recrea vacío y se re-autoriza (ver `x-reauth.md`).
5. Webhooks: se crean al importar los escenarios que los usan; actualizar las URLs nuevas en el sitio (formularios de prensa y 1-click) y en la app de X.
6. Escenarios: importar desde `make/scenarios/` en este orden: utilitarios → scanners → Publisher → gate vigilante → Social → Brief. En cada módulo, re-vincular conexión y data store (los IDs internos cambian).
7. Reemplazar IDs viejos en tareas programadas y skills (`runbooks/scheduled-tasks.md`).
8. Activar schedules y correr Publisher con una fila de prueba.

Prioridad si no hay tiempo para todo: Publisher + scanners + gate vigilante. Brief y Social pueden esperar un día.
