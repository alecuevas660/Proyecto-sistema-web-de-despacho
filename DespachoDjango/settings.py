LOGIN_REDIRECT_URL = '/'  # Redirige a la ruta raíz después del login
LOGIN_URL = 'login'  # URL para el login
LOGOUT_REDIRECT_URL = 'login'  # URL después del logout

# Configuraciones de sesión (opcional pero recomendado)
SESSION_COOKIE_AGE = 86400  # Duración de la sesión en segundos (24 horas)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # La sesión persiste aunque se cierre el navegador