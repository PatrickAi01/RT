from django.core.management.utils import get_random_secret_key
from pathlib import Path
import os, sys#, dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True #for development only, comment out in deployment and uncomment bottom code
#DEBUG = os.getenv('DEBUG', 'False') == 'True'



ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
if not DEBUG:
    ALLOWED_HOSTS += [os.environ.get('DJANGO_ALLOWED_HOST')]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'websets',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "RTAwebsite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "RTAwebsite.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


#development db (sqlite-saved locally)
if DEBUG is True:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }

""" 
elif len(sys.argv) > 0 and sys.argv[1] != 'collectstatic':
    if os.getenv("DATABASE_URL", None) is None:
        raise Exception("DATABASE_URL environment variable not defined")
    DATABASES = {
        "default": dj_database_url.parse(os.environ.get("DATABASE_URL")),
        
    }
make this work?
"""

"""
#development database
if DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),  # Replace with the desired database name
        }
    }
else:
    
    POSTGRES_DB = os.environ.get("db")
    POSTGRES_PASSWORD = os.environ.get("AVNS_5LxrmzcLJWrTcebwiv0")
    POSTGRES_USER = os.environ.get("db")
    POSTGRES_HOST = os.environ.get("app-8551d3b6-dafc-4f29-9fb4-5467fbc7c822-do-user-14476911-0.b.db.ondigitalocean.com")
    POSTGRES_PORT = os.environ.get("25060")

    POSTGRES_READY = (
        POSTGRES_DB is not None
        and POSTGRES_PASSWORD is not None
        and POSTGRES_USER is not None
        and POSTGRES_HOST is not None
        and POSTGRES_PORT is not None
    )

    if POSTGRES_READY:"""
"""
#production db (postgresql - saved in digitalocean db)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "db",
        "USER": "db",
        "PASSWORD": "AVNS_5LxrmzcLJWrTcebwiv0",
        "HOST": "app-8551d3b6-dafc-4f29-9fb4-5467fbc7c822-do-user-14476911-0.b.db.ondigitalocean.com",
        "PORT": "25060",
        }
    }
"""


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"),]



# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

#youtube api
API_KEY = '618c641402msh87f3cbb65fc2a64p16e8f2jsn2685ae2145b5'
API_HOST = 'youtube-mp36.p.rapidapi.com'