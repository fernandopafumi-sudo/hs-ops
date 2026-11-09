# Mapa de dependencias de Make (generado desde el backup)

Regenerar con `python3 scripts/gen_ids.py` después de cada backup. Las referencias desde tareas programadas de Claude y skills están en `runbooks/scheduled-tasks.md`.

## Escenarios

| ID | Nombre | Estado | Schedule | Data stores | Hooks | IDs de escenarios citados | Apps |
|---|---|---|---|---|---|---|---|
| 5096381 | HealthSignals- Intelligence Scanner | ON | weekly:07:00 | 148747 HS Event Dedup |  |  | anthropic-claude, builtin, datastore, exa-ai, google-sheets, json, util |
| 5133643 | PROD Article Publisher v2 | ON | daily:06:40 |  |  |  | airtable, anthropic-claude, builtin, exa-ai, google-sheets, http, json, openai-gpt-3, util, wordpress |
| 5167429 | HS Social Publisher v2 | off | indefinitely:10800 | 128118 X OAuth - HealthSignals |  | 5882000 | datastore, google-sheets, http, linkedin, regexp, util |
| 5453337 | HS Outreach A - Draft Generator | ON | on-demand |  |  |  | airtable, anthropic-claude, util |
| 5453401 | HS Outreach B - Sender | ON | on-demand |  |  |  | airtable, resend |
| 5453897 | HS LinkedIn Draft Engine | off | indefinitely:86400 |  |  |  | airtable, anthropic-claude, builtin, http, util |
| 5454484 | HS Weekly Digest | off | indefinitely:604800 |  |  |  | anthropic-claude, builtin, http, util, wordpress |
| 5699954 | HS Report — Proposer | ON | on-demand |  |  |  | airtable, anthropic-claude |
| 5841829 | LB — Group Post Reminder (620 Spend A Buck) | off | daily:09:00 |  |  |  | airtable, resend |
| 5843912 | HS Prospect Search - LinkedIn LATAM | off | immediately |  | 2656053 |  | airtable, builtin, gateway |
| 5882000 | HS X OAuth Setup | ON | immediately | 128118 X OAuth - HealthSignals | 2666530 |  | datastore, gateway, http |
| 5886398 | HS WordPress to Airtable Sync | off | weekly:08:00 |  |  |  | airtable, builtin, http |
| 5890585 | HS LinkedIn CRM Loader — Execute Now | ON | on-demand |  |  |  | airtable, builtin |
| 5890673 | HS LinkedIn Import → CRM Sync | off | on-demand |  |  |  | airtable |
| 5891229 | Extract Prospects from Published Articles | off | on-demand |  |  |  | airtable, anthropic-claude, builtin |
| 5893513 | HS Price Feeds — listas oficiales de precios | ON | monthly:06:00 |  |  |  | airtable, builtin, http, regexp, util |
| 6070111 | HealthSignals - Thematic Scanner (Topic Registry) | ON | on-demand |  |  |  | anthropic-claude, builtin, exa-ai, google-sheets, json, util |
| 6202822 | HS - Sheet Ops (ad-hoc) | ON | on-demand | 124602 sec_ticker_cache |  |  | datastore, google-sheets |
| 6233803 | HS Brief — Composer (WIP) | ON | on-demand |  |  |  | airtable, anthropic-claude, builtin, http, util |
| 6234149 | HS Brief — Render Test | ON | on-demand |  |  |  | airtable, http, util, wordpress |
| 6234307 | HS Brief — Production | ON | on-demand |  |  | 6427153 | airtable, anthropic-claude, builtin, http, json, util, wordpress |
| 6234838 | HS Brief — Email Test | ON | on-demand |  |  |  | http, util |
| 6234915 | HS Brief — Email Send | ON | weekly:07:00 |  |  |  | airtable, http, json, util |
| 6245658 | HS - Unstick processing rows | ON | on-demand |  |  |  | google-sheets |
| 6245964 | HS - Approve queue rows (ad-hoc) | ON | on-demand |  |  |  | google-sheets |
| 6246530 | HS - Park approved backlog | ON | on-demand |  |  |  | google-sheets |
| 6248217 | HS - Queue snapshot to datastore | ON | on-demand | 148918 HS Queue Snapshot |  |  | builtin, datastore, google-sheets |
| 6251333 | HS - Skip rows for social (ad-hoc) | ON | on-demand |  |  |  | google-sheets |
| 6251400 | HS - Scanner rows snapshot (last batch) | ON | on-demand | 148918 HS Queue Snapshot |  |  | builtin, datastore, google-sheets |
| 6263946 | HS — SEO Rank Tracker (GSC weekly) | ON | weekly:08:00 |  |  |  | google-search-console, google-sheets |
| 6313594 | HS — Featured image por post ID | ON | on-demand |  |  |  | anthropic-claude, builtin, json, openai-gpt-3, util, wordpress |
| 6314042 | HS — Guard imagen destacada (watchdog) | ON | indefinitely:10800 |  |  |  | anthropic-claude, builtin, http, json, openai-gpt-3, util, wordpress |
| 6414510 | [BORRAR] HS test 6414510 | off | on-demand |  |  |  | anthropic-claude, builtin, google-drive, json, openai-gpt-3, util |
| 6424186 | [BORRAR] HS test cover fix 6424186 | off | on-demand |  |  |  | anthropic-claude, builtin, google-drive, google-sheets, http, json, openai-gpt-3, util, wordpress |
| 6424598 | [BORRAR] HS test 6424598 | off | on-demand |  |  |  | google-drive, util |
| 6426906 | [BORRAR] HS UTIL view images 6426906 | off | on-demand |  |  |  | builtin, google-drive, http, util |
| 6427153 | HS Brief — Render from reviewed content | ON | on-demand |  |  |  | airtable, http, json, util, wordpress |
| 6459598 | HS Brief Subscribers | ON | immediately |  | 2876709 |  | airtable, builtin, gateway, json, sendinblue |
| 6460310 | HS Brief Subscribers — Sync confirmados (Brevo → Airtable) | ON | indefinitely:21600 |  |  |  | airtable, builtin, sendinblue |
| 6461147 | HS gate vigilante (capa 2) | ON | daily:09:00 | 161375 HS gate state (capa 2) |  |  | datastore, resend |
| 6488206 | HS MedTech Tracker — FDA → Brasil/Colombia (mensual) | ON | monthly:07:10 |  |  |  | airtable, builtin, code, http, util |
| 6508650 | HS Social Publisher v3 | ON | weekly:08:40 | 128118 X OAuth - HealthSignals, 164495 HS LinkedIn shared posts |  | 5882000 | builtin, datastore, google-sheets, http, linkedin, util |
| 6543177 | HS - Auto-approve 1 high draft/day | ON | daily:06:30 |  |  |  | google-sheets |
| 6674701 | HS Press Signup — página de prensa → Airtable | ON | immediately |  | 2948578 |  | airtable, builtin, gateway, resend |
| 6721172 | HS - FDA Approvals Scanner (RSS) | ON | daily:06:41 | 148747 HS Event Dedup |  |  | anthropic-claude, builtin, datastore, google-sheets, json, rss, util |
| 6724293 | HS - Events Scanner (congresos y cumbres) | ON | daily:07:23 | 148747 HS Event Dedup |  |  | anthropic-claude, builtin, datastore, exa-ai, google-sheets, json, util |
| 6725295 | HS - Auto-approve top policy/approvals/eventos (lun+jue) | ON | weekly:06:20 |  |  |  | google-sheets, util |
| 6726530 | HS Brief Approvals (webmail aprobados por Fer) | ON | indefinitely:21600 |  |  |  | airtable, builtin, sendinblue |
| 6735926 | HS - Cover for manual post (ad-hoc) | ON | on-demand |  |  |  | anthropic-claude, builtin, google-sheets, http, json, openai-gpt-3, util, wordpress |
| 6828787 | HS - Set queue status by row (ad-hoc) | ON | on-demand | 187494 HS row lookup (ad-hoc) |  |  | datastore, google-sheets |
| 6841390 | TEST Publisher v2 - Evidencia C (fila 606) | ON | on-demand |  |  |  | airtable, anthropic-claude, builtin, exa-ai, google-sheets, http, json, openai-gpt-3, util, wordpress |
| 6854895 | HS Invite 1-click subscribe (Brief) | ON | immediately |  | 3008026 |  | airtable, builtin, gateway, sendinblue, util |
| 6856433 | HS — Brevo: quitar internos de lista 5 (ad hoc) | off | on-demand |  |  |  | sendinblue |

## Data stores → escenarios que los usan

| ID | Nombre | Usado por |
|---|---|---|
| 103109 | ClaudeMonitor_HistoricalMetrics | ningún escenario (verificar tareas de Claude) |
| 124602 | sec_ticker_cache | 6202822 |
| 128118 | X OAuth - HealthSignals | 5167429, 5882000, 6508650 |
| 128466 | HS LinkedIn Contacts Import | ningún escenario (verificar tareas de Claude) |
| 148747 | HS Event Dedup | 5096381, 6721172, 6724293 |
| 148918 | HS Queue Snapshot | 6248217, 6251400 |
| 161375 | HS gate state (capa 2) | 6461147 |
| 162492 | HS Voices Rules | ningún escenario (verificar tareas de Claude) |
| 164495 | HS LinkedIn shared posts | 6508650 |
| 187494 | HS row lookup (ad-hoc) | 6828787 |

## Conexiones → escenarios

| ID | Nombre | Escenarios |
|---|---|---|
| 8455399 | My Google Restricted connection | 0:  |
| 8921729 | My WordPress connection | 10: 5133643, 5454484, 6234149, 6234307, 6313594, 6314042, 6424186, 6427153, 6735926, 6841390 |
| 8921875 | My LinkedIn connection | 0:  |
| 8922808 | My Anthropic Claude connection | 7: 5133643, 5453337, 5699954, 5891229, 6313594, 6314042, 6841390 |
| 8923111 | My Anthropic Claude connection | 6: 5096381, 6070111, 6233803, 6234307, 6721172, 6724293 |
| 8923977 | My Google connection | 21: 5096381, 5133643, 5167429, 6070111, 6202822, 6245658, 6245964, 6246530, 6248217, 6251333, 6251400, 6263946, 6424186, 6508650, 6543177, 6721172, 6724293, 6725295, 6735926, 6828787, 6841390 |
| 8943313 | My OpenAI connection | 7: 5133643, 6313594, 6314042, 6414510, 6424186, 6735926, 6841390 |
| 8944176 | My OpenAI connection | 0:  |
| 8981470 | My Todoist connection | 0:  |
| 8984010 | My Exa connection | 5: 5096381, 5133643, 6070111, 6724293, 6841390 |
| 9040242 | LinkedIn - HealthSignals Company Page | 2: 5167429, 6508650 |
| 9132003 | My Airtable Token or Key connection | 22: 5133643, 5453337, 5453401, 5453897, 5699954, 5841829, 5843912, 5886398, 5890673, 5893513, 6233803, 6234149, 6234307, 6234915, 6427153, 6459598, 6460310, 6488206, 6674701, 6726530, 6841390, 6854895 |
| 9533217 | Resend HealthSignals | 4: 5453401, 5841829, 6461147, 6674701 |
| 11075018 | Fernando's Google Search Console connection | 1: 6263946 |
| 11340939 | Google Drive editor@ (full) | 4: 6414510, 6424186, 6424598, 6426906 |
| 11417335 | Fernando's Brevo connection | 5: 6459598, 6460310, 6726530, 6854895, 6856433 |

## Webhooks

| ID | Nombre | Escenario |
|---|---|---|
| 2656053 | HS Prospect Search Webhook | 5843912 |
| 2666530 | X OAuth Callback - HealthSignals | 5882000 |
| 2876709 | HS Brief Subscribers (web CTA) | 6459598 |
| 2948578 | HS Press Signup (página prensa) | 6674701 |
| 3008026 | HS Invite 1-click subscribe | 6854895 |
