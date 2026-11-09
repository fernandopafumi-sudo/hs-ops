# Re-autorizar X (Twitter)

Síntoma: Social Publisher v3 (6508650) deja de postear en X; el data store 164495 tiene `last_error` con "reautorizar con scenario 5882000", o el refresh token venció.

Por qué pasa: el refresh token de X rota en cada uso. Si un refresh se consume y la escritura en el data store 128118 falla, queda inválido.

Pasos:
1. Activar el escenario 5882000 "HS X OAuth Setup". **Nunca borrarlo ni borrar su webhook**: la URL de ese webhook es el redirect_uri registrado en la app de X.
2. Abrir el link de autorización de X (client_id en Bitwarden, entrada "X app"), loguearse como la cuenta de HealthSignals y aceptar.
3. El webhook recibe el code, lo canjea y guarda el token nuevo en 128118.
4. Desactivar 5882000.
5. Correr Social Publisher v3 a mano y confirmar el post.

client_id y client_secret: Bitwarden. No se respaldan en este repo.
