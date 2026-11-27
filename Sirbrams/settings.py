import os
from pathlib import Path
from decouple import config
import environ


# Initialize environment variables
env = environ.Env()
environ.Env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')

# Production is the default. Set DEBUG=True in your local .env while developing.
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = [
    "sirbrams-branding.onrender.com",
    "localhost",
    "127.0.0.1"
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'TechApp',
    "anymail",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Sirbrams.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Sirbrams.wsgi.application'

# Where the database and admin uploads live. Locally this is the project folder.
# On Render, attach a persistent disk and set DATA_DIR to its mount path
# (for example /var/data); otherwise uploads and the database are wiped on
# every deploy.
DATA_DIR = Path(config('DATA_DIR', default=str(BASE_DIR)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DATA_DIR / 'db.sqlite3',
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'  # Changed to Nairobi timezone

USE_I18N = True

USE_TZ = True

# Files uploaded from the admin panel (portfolio images).
MEDIA_URL = '/media/'
MEDIA_ROOT = DATA_DIR / 'media'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = False

CSRF_TRUSTED_ORIGINS = [
    'https://sirbrams-branding.onrender.com',
    'http://127.0.0.1:8000',
    'http://localhost:8000'
]
# 📧 Email (Brevo via HTTP API)
EMAIL_BACKEND = "anymail.backends.brevo.EmailBackend"

ANYMAIL = {
    "BREVO_API_KEY": config("BREVO_API_KEY", default=""),
}

DEFAULT_FROM_EMAIL = "SirBrams Support <sirbramstechcampus1@gmail.com>"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

