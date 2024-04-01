"""
Django settings for villager_chess project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
# from dotenv import load_dotenv GOOGLE THIS. IT CAN BE USED TO ADD ENVIRONMENT VARIABLES TO THE SETTINGS.PY
from pathlib import Path
import os
import django_on_heroku
from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-xw8gkue0a=_wma%rcc*$)i-3%(h71!lj&mpuc1c0#8&rgkv$l_'
# SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []


# Application definition


# UPDATE THIS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'villager_chess_api',
    # 'openai'
]

# THIS IS NEW
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# THIS IS NEW
CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    # 'http://localhost:3051', # Added Nginx server address and port
    # 'http://127.0.0.1:3051', # Added Nginx server address and port
    'http://localhost:3050', # Added Nginx server address and port
    'http://127.0.0.1:3050', # Added Nginx server address and port
    # 'https://6470c208d361a40009ceab9e--visionary-treacle-0efacd.netlify.app',
    'https://loquacious-bienenstitch-cc2290.netlify.app',
    # 'https://visionary-treacle-0efacd.netlify.app'
    'https://villagerchess.netlify.app'
]
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    # 'http://localhost:3051', # Added Nginx server address and port
    # 'http://127.0.0.1:3051', # Added Nginx server address and port
    'http://localhost:3050', # Added Nginx server address and port
    'http://127.0.0.1:3050', # Added Nginx server address and port
    'https://loquacious-bienenstitch-cc2290.netlify.app',
    'https://villagerchess.netlify.app'
]

# UPDATE THIS
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# # MY OWN ADDED SETTING FOR AI
# CSRF_TRUSTED_ORIGINS = [
#     'http://localhost:3000',
#     'http://127.0.0.1:3000'
# ]


ROOT_URLCONF = 'villager_chess.urls'

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

WSGI_APPLICATION = 'villager_chess.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
if os.getenv('CONTAINER')=='local':
  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
if os.getenv('CONTAINER')=='docker':
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'docker.sqlite3',
    }
# Override with PostgreSQL settings if environment variables are set
# NEED TO ADDRESS USAGE OF GUEST USER BEFORE ABLE TO CREATE DATABASE FROM SCRATCH IN DOCKER BUILD
# NEED TO PIP INSTALL PYTHON-DECOUPLE IF YOU GO THIS ROUTE
# if os.environ.get('DATABASE_ENGINE'):
#     DATABASES['default'] = {
#         'ENGINE': config('DATABASE_ENGINE'),
#         'NAME': config('DATABASE_NAME'),
#         'USER': config('DATABASE_USER'),
#         'PASSWORD': config('DATABASE_PASSWORD'),
#         'HOST': config('DATABASE_HOST'),
#         'PORT': config('DATABASE_PORT'),
#     }
# if os.environ.get('DATABASE_ENGINE'):
#     print('using docker db')
#     DATABASES['default'] = {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'docker.sqlite3',
#     }




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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# old static url commented out before deploy
# STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# below added for deploy
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = "/static/"
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

django_on_heroku.settings(locals())