import os
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get('DEBUG', default=0))

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS').split(' ')

AUTH_USER_MODEL = 'useraccount.User' #permite que el modelo de usuario se pueda usar

SITE_ID = 1 #id del sitio web: 

WEBSITE_URL = 'localhost:8000' #url del sitio web

#configuración de simplejwt: permite que los usuarios se autentiquen con tokens
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': True,
    'SIGNING_KEY': "acomplexkey",
    'ALGORITHM': 'HS512',
}

#configuración de allauth: permite que los usuarios se registren y autentiquen
ACCOUNT_USER_MODEL_USERNAME_FIELD = None 
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'

#configuración de rest_framework: permite que los usuarios se autentiquen con el framework de django
# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     ),
#     'DEFAULT_PERMISSION_CLASSES': (
#         'rest_framework.permissions.IsAuthenticated', 
#     ),
# }

#Configuracion sin permisos de logeo para desarrollo fluido
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}

#configuración de cors: permite que el frontend se comunique con el backend
CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:3000', 
    'http://127.0.0.1:8000',
    "http://localhost:3000",
]

#configuración de rest_auth: permite que los usuarios se autentiquen
REST_AUTH = {
    'USE_JWT': False, #True para usar JWT y False para usar tokens
    'JWT_AUTH_HTTPONLY': False,
}

#configuración de las aplicaciones instaladas: son las aplicaciones que se van a usar en el proyecto
INSTALLED_APPS = [
    'django.contrib.admin', 
    'django.contrib.auth', 
    'django.contrib.contenttypes', 
    'django.contrib.sessions', 
    'django.contrib.messages', 
    'django.contrib.staticfiles', 
    
    'rest_framework', 
    'rest_framework.authtoken', 
    'rest_framework_simplejwt', 
    
    'allauth', 
    'allauth.account', 
    
    'dj_rest_auth', 
    'dj_rest_auth.registration', 
    
    'corsheaders', 
    
    'product', 
    'useraccount', 
]

#configuración de los middlewares: son funciones que se ejecutan antes de que se procese una solicitud
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

#configuración de la url principal: es la url que se va a usar para acceder a la aplicación
ROOT_URLCONF = 'django_backend.urls'

#configuración de los templates: un template es una plantilla de html que se puede usar para renderizar una vista
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

#configuración de la aplicación de wsgi: es la aplicación que se va a usar para servir la aplicación

WSGI_APPLICATION = 'django_backend.wsgi.application'

#configuración de la base de datos: es la base de datos que se va a usar para almacenar los datos
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('SQL_ENGINE'),
        'NAME': os.environ.get('SQL_DATABASE'),
        'USER': os.environ.get('SQL_USER'),
        'PASSWORD': os.environ.get('SQL_PASSWORD'),
        'HOST': os.environ.get('SQL_HOST'),
        'PORT': os.environ.get('SQL_PORT'),
    }
}

#configuración de las validaciones de contraseña: son validaciones que se van a usar para validar las contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

#configuración de la codificación de caracteres: es la codificación de caracteres que se va a usar para el proyecto
LANGUAGE_CODE = 'es-mx'

#configuración de la zona horaria: es la zona horaria que se va a usar para el proyecto
TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

#configuración de los archivos estáticos: son los archivos que se van a usar para servir la aplicación
STATIC_URL = 'static/'
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

#configuración del campo de clave primaria: es el campo de clave primaria que se va a usar para el proyecto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

