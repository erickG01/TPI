"""
Django settings for TPI_PROJECT project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""


from pathlib import Path
import dj_database_url
from dotenv import load_dotenv
import os

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# Para cliente
#PWA_CLIENTE_SERVICE_WORKER = os.path.join(BASE_DIR, 'static/js','serviceworker-cliente.js')
# Para repartidor
#PWA_REPARTIDOR_SERVICE_WORKER = os.path.join(BASE_DIR, 'static/js','serviceworker-repartidor.js')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-gwmrj669pw^#v+!ebk-m6)=kznj_xyt2wb@gqdlsotxk)9g32o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


#Pruebas para NGROK
# CSRF_TRUSTED_ORIGINS = [
#      #Recuerden que ngrok da una direccion que es dinamica asi que ojo
#      'https://dd56-179-60-173-76.ngrok-free.app'
#  ]
CSRF_TRUSTED_ORIGINS = [
    'https://tpi115proyecto-production.up.railway.app',
    'http://127.0.0.1',
    'https://5216-190-99-43-6.ngrok-free.app',
    'https://web-production-6242f.up.railway.app'

]




# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic',
    'django.contrib.sites', #necesario para django pwa
    'Cliente',
    'Repartidor',
    'Negocio',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]

ROOT_URLCONF = 'TPI_PROJECT.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
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

WSGI_APPLICATION = 'TPI_PROJECT.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}

SITE_ID = 1

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
# Para archivos media de base de datos
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

#Consumir los cambios de colores
COLOR_FILE = os.path.join(BASE_DIR,'config','color_scheme.json')

#whitenoise
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
# settings.py
SESSION_COOKIE_AGE = 3600  # Tiempo de inactividad en segundos (ejemplo: 5 minutos)
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # La sesión expira cuando se cierra el navegador


#redirect
LOGIN_REDIRECT_URL = 'comida'

LOGIN_URL = 'editar_cliente/'



#configuracion para pwa cliente

#Configuracion de envio de correo
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tpi115gp05@gmail.com'
EMAIL_HOST_PASSWORD = 'didq nosq rlng qvzm'
DEFAULT_FROM_EMAIL = 'tpi115gp05@gmail.com'

# settings.py
#CSRF_TRUSTED_ORIGINS = [
 #   'https://a0ed-2800-b20-1113-bb4-dc9e-ef15-3077-8c05.ngrok-free.app'
#]
