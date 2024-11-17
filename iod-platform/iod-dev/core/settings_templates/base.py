import os, environ
from pathlib import Path
from dotenv import load_dotenv


#load env variables from env
load_dotenv()

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, True)
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = Path(CORE_DIR)
CORE_DIR = path.parent.absolute()
print("core directory path is :"+str(CORE_DIR))

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='S#perS3crEt_007')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

# Assets Management
ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets') 

# load production server from .env
ALLOWED_HOSTS        = ['localhost', 'localhost:85', '127.0.0.1',               env('SERVER', default='127.0.0.1') ]
CSRF_TRUSTED_ORIGINS = ['http://localhost:85', 'http://127.0.0.1', 'https://' + env('SERVER', default='127.0.0.1') ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.home',                                    # Enable the inner home (home)
    'apps.configuration',
    'apps.demo',
    'apps.esite',
    'apps.extsite',
    # 'allauth',                                      # OAuth new
    # 'allauth.account',                              # OAuth new
    # 'allauth.socialaccount',                        # OAuth new 
    # 'allauth.socialaccount.providers.github',       # OAuth new 
    # 'allauth.socialaccount.providers.twitter',      # OAuth new  
    
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

ROOT_URLCONF = 'core.urls'
LOGIN_REDIRECT_URL = "home"  # Route defined in home/urls.py
LOGOUT_REDIRECT_URL = "landing_page"  # Route defined in home/urls.py
TEMPLATE_DIR = os.path.join(CORE_DIR, "apps/templates")  # ROOT dir for templates
print("templates directory path is :"+str(TEMPLATE_DIR))
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.context_processors.cfg_assets_root',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#############################################################
# SRC: https://devcenter.heroku.com/articles/django-assets

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(CORE_DIR, 'static')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(CORE_DIR, 'apps/static'),
    os.path.join(CORE_DIR, 'apps/static/assets/phoenix_theme/frontend/public'),
) 

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# EMAIL Settings

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')

print("DEFAULT_FROM_EMAIL is set to :"+DEFAULT_FROM_EMAIL)

if os.getenv('SMTP_SERVER') == 'prod':
    print("---Cofigured Production SMTP Server for sending emails---")
    EMAIL_HOST = env('EMAIL_HOST')
    EMAIL_PORT = env('EMAIL_PORT')
    EMAIL_HOST_USER = env('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
elif os.getenv('SMTP_SERVER') == 'qa':
    print("---Cofigured QA Googie SMTP Server for sending emails---")
    EMAIL_HOST = env('EMAIL_HOST')
    EMAIL_PORT = env('EMAIL_PORT')
    EMAIL_HOST_USER = env('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
else:  # For local development
    print("---Cofigured Local SMTP Server for sending emails---")
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 8025
    EMAIL_USE_TLS = False


# Logging Settings
import logging
from logging.handlers import TimedRotatingFileHandler

# Get the environment variable value
ENV = os.getenv('SDIARY_ENV')

# Set the logging level based on the environment
if ENV == 'dev':
    LOG_LEVEL = 'DEBUG'
elif ENV == 'qa':
    LOG_LEVEL = 'INFO'
elif ENV == 'prod':
    LOG_LEVEL = 'WARNING'
elif ENV == 'uat':
    LOG_LEVEL = 'WARNING'
else:
    LOG_LEVEL = 'WARNING'

LOGGER_ROOT = os.path.join(CORE_DIR, 'logs/iod-server.log')
print("Logger root is : "+ LOGGER_ROOT)
print("Loading log level : "+LOG_LEVEL + " as per env : "+ENV)
LOGGING = {
    'formatters': {
    'verbose': {
        'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S',
    },
    },
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': LOG_LEVEL,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': LOGGER_ROOT,
            'when': 'midnight',
            'interval': 1,
            'backupCount': 366,
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': LOG_LEVEL,
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
    },
}

# settings.py

# Celery Configuration Options
CELERY_TIMEZONE = "Asia/Kolkata"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

DEV_MODE = os.getenv('DEV_MODE') 

if DEV_MODE == 'WEB':
    # iod-web setting
    CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Redis URL
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'  # Store task results in Redis
elif DEV_MODE == 'FUSION':
    # pdf fusion setting
    CELERY_BROKER_URL = 'redis://redis:6379/0'  # Use the Redis service name
    CELERY_RESULT_BACKEND = 'redis://redis:6379/0'

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TIMEZONE = 'UTC'
