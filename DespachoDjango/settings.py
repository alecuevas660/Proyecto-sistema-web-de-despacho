LOGIN_REDIRECT_URL = '/'  # Redirige a la ruta raíz después del login
LOGIN_URL = 'login'  # URL para el login
LOGOUT_REDIRECT_URL = 'login'  # URL después del logout

# Configuraciones de sesión (opcional pero recomendado)
SESSION_COOKIE_AGE = 86400  # Duración de la sesión en segundos (24 horas)
# La sesión persiste aunque se cierre el navegador
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Configuraciones del envio de correos con gmail
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tu_correo@gmail.com'
EMAIL_HOST_PASSWORD = 'tu_contraseña'
DEFAULT_FROM_EMAIL = 'tu_correo@gmail.com'
