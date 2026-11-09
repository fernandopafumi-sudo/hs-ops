# Cuentas y recuperación

Punto único de falla: la cuenta de Google Workspace editor@healthsignals.news. De ella cuelgan la Editorial Queue, Gmail de las tareas, Drive, y el login de varias herramientas.

| Servicio | Login | Recuperación | 2FA | Códigos en Bitwarden |
|---|---|---|---|---|
| Google Workspace (editor@) | editor@healthsignals.news | fernandopafumi@gmail.com + teléfono; segundo super-admin (pendiente) | pendiente verificar | pendiente |
| GitHub | fernandopafumi-sudo | backup email Gmail personal | pendiente (passkey) | pendiente |
| Make | verificar | | | |
| Airtable | verificar | | | |
| WordPress.com (sitio, dominio, DNS) | verificar | fernandopafumi@gmail.com | | |
| Brevo | verificar | | | |
| Resend | verificar | | | |
| X (app y cuenta) | verificar | | | |
| LinkedIn company page | perfil de Fer (admin) | segundo admin (pendiente) | | |
| Anthropic / OpenAI / Exa / PDFShift | verificar | | | |
| Bitwarden | Gmail personal | contraseña maestra en papel, en casa | sí | — |

Reglas:
- Ninguna contraseña ni token en este repo, en Drive ni en chats. Solo Bitwarden.
- Tokens de backup (Make, Airtable, espejo): solo lectura, rotación cada 90 días.
- Si Google suspende editor@: entrar a admin.google.com con el segundo super-admin, revisar el motivo en el registro de auditoría, reactivar. Mientras tanto, pausar la tarea de invitaciones al Brief (es la causa más probable: envío masivo desde Gmail).

## Recuperar Google Workspace sin segundo admin
admin.google.com → "¿Olvidaste la contraseña?" → verificación por el email/teléfono de recuperación. Si no hay ninguno: soporte de Google con verificación de dominio por DNS (registro TXT en WordPress.com). Toma días: por eso el segundo admin es prioridad.
