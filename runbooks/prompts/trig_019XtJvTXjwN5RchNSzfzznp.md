SIN NAVEGADOR (decisión de Fer, 09-11-2026): esta tarea no usa navegador ni computadora: nada de Claude in Chrome, Claude_Browser ni computer use, y no existe el servidor hs-cloud-01. Lo que antes se publicaba o enviaba por navegador en LinkedIn o X ahora lo hace Fer a mano desde el teléfono: dejáselo listo en el mensaje (link solo en su línea para tocarlo y abrir la app; texto a pegar en un bloque de código; para comentarios, recordale 'Comentar como HealthSignals'). Cuando Fer confirme en el chat ('listo', 'publiqué', 'mandé' o pegue la URL), registrá lo hecho en Airtable como antes. Los mails se envían por el conector de Gmail (send_message / reply), nunca abriendo Gmail en un navegador.

Voices de HealthSignals: enviar ahora (12:15 UTC del 18-11; Fer, Fernando Pafumi, lo aprobó el 17-10) la invitación a Rudi Rocha (FGV). Creado el 01-11-2026 al pasar las tareas de la PC con Windows a la nube; reemplaza al recordatorio "Rocha: enviar invitación Voices 12:15 UTC" del 17-10. Español informal con Fer, sin negritas ni headers.

Datos: cuenta editor@healthsignals.news. Borrador Gmail r-2927745557532935723 a rudi.rocha@fgv.br, hilo 1a144b2a584dd526 (o el vigente en Gmail_Draft_ID). Airtable base appjkRayvA0YEjczd, tabla Voices Pipeline tblCnK5agV3rVKGnl, registro recX7E0BcuoDLwTqb.

Chequeo previo obligatorio (si algo falla, NO envíes y avisá a Fer):
1. El borrador existe, el saludo es exactamente "Prezado Professor Rudi Rocha,", el Word está adjunto.
2. La re-verificación del 17-11 no dejó ninguna premisa caída sin OK de Fer (mirá Notes del registro y si Fer escribió algo al respecto).
3. Regla de Fer del 19-10: sin CC a fernandopafumi@gmail.com. Si el borrador tiene ese CC o links google.com/url, recrealo con create_draft sin ese CC y con links limpios, adjuntando el Word descargado de Drive (campo Docx_Drive_ID), verificá adjunto y CC con get_draft, borrá el viejo y actualizá Gmail_Draft_ID.

Si todo está OK: enviá con send_message(draftId) del conector de Gmail y actualizá el registro (Stage Sent, Email_Status, Touches, Notes con el message id). Avisale a Fer en una línea.