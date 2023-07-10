"""
Django settings for stude project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from dotenv import load_dotenv  # Python dotenv
import os


load_dotenv()  # loads the configs from .env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.getenv('SECRET_KEY'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*', '127.0.0.1', 'localhost', '10.0.10.32', '10.0.10.8']

# Email credentials
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = ''
EMAIL_USE_TLS = False

if (DEBUG == True):
    EMAIL_HOST = str(os.getenv('DEV_EMAIL_HOST'))
    EMAIL_HOST_USER = str(os.getenv('DEV_EMAIL_HOST_USER'))
    EMAIL_HOST_PASSWORD = str(os.getenv('DEV_EMAIL_HOST_PASSWORD'))
    EMAIL_PORT = str(os.getenv('DEV_EMAIL_PORT'))
else:
    EMAIL_HOST = str(os.getenv('PROD_EMAIL_HOST'))
    EMAIL_HOST_USER = str(os.getenv('PROD_EMAIL_HOST_USER'))
    EMAIL_HOST_PASSWORD = str(os.getenv('PROD_EMAIL_HOST_PASSWORD'))
    EMAIL_PORT = str(os.getenv('PROD_EMAIL_PORT'))
    EMAIL_USE_TLS = str(os.getenv('PROD_EMAIL_TLS'))

# Will need to install OSGeo4W for this!
if os.name == 'nt':
    OSGEO4W = r"C:\OSGeo4W"
    if not os.path.isdir(OSGEO4W):
        OSGEO4W += '64'
    os.environ['OSGEO4W_ROOT'] = OSGEO4W
    os.environ['GDAL_DATA'] = "C:\Program Files\GDAL\gdal-data"
    os.environ['PROJ_LIB'] = OSGEO4W + r"\share\proj"
    GDAL_LIBRARY_PATH = r'C:\OSGeo4W64\bin\gdal204'
    os.environ['PATH'] = OSGEO4W + r"\bin;" + os.environ['PATH']

GEOS_LIBRARY_PATH = str(os.environ.get('VIRTUAL_ENV') +
                        r"\Lib\site-packages\osgeo\geos_c.dll")
GDAL_LIBRARY_PATH = str(os.environ.get('VIRTUAL_ENV') +
                        r"\Lib\site-packages\osgeo\gdal304.dll")

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'rest_framework',
    'rest_framework_simplejwt',
    'djoser',
    'accounts',
    'student_status',
    'courses',
    'year_levels',
    'semesters',
    'subjects',
    'study_groups',
    'studygroup_messages',
    'leaflet',
    'landmarks',
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
]

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

ROOT_URLCONF = 'config.urls'

ASGI_APPLICATION = "config.asgi.application"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

"""DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}"""

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.spatialite',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_USER_MODEL = 'accounts.CustomUser'

DJOSER = {
    'SEND_ACTIVATION_EMAIL': True,
    'SEND_CONFIRMATION_EMAIL': True,
    'EMAIL': {
        'activation': 'config.email.ActivationEmail'
    },
    'ACTIVATION_URL': 'activation/{uid}/{token}',
    'USER_AUTHENTICATION_RULES': ['djoser.authentication.TokenAuthenticationRule'],
    'SERIALIZERS': {
        'user': 'accounts.serializers.CustomUserSerializer',
        'current_user': 'accounts.serializers.CustomUserSerializer',
        'user_create': 'accounts.serializers.UserRegistrationSerializer',
    },
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Manila'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DOMAIN = ''
if (DEBUG):
    DOMAIN = 'exp'
else:
    DOMAIN = 'stude'


SITE_NAME = 'Stud-E'

JWT_TOKEN_LIFETIME = 10800
ACCESS_TOKEN_LIFETIME = JWT_TOKEN_LIFETIME
REFRESH_TOKEN_LIFETIME = 24 * JWT_TOKEN_LIFETIME

LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (8.48567, 124.65642),
    'DEFAULT_ZOOM': 19,
    'MAX_ZOOM': 20,
    'MIN_ZOOM': 3,
    'SCALE': 'both'
}
