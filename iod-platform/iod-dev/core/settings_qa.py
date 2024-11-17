from core.settings_templates.base import *
from core.settings_templates.database import *

# load production server from .env
ALLOWED_HOSTS        = ['172.24.217.125','localhost', 'localhost:85', '127.0.0.1',               env('SERVER', default='127.0.0.1') ]
CSRF_TRUSTED_ORIGINS = ['http://172.24.217.125/','http://localhost:85', 'http://127.0.0.1', 'https://' + env('SERVER', default='127.0.0.1') ]


if os.environ.get('DB_ENGINE') and os.environ.get('DB_ENGINE') == "mysql":
    DATABASES = { 
      'default': {
        'ENGINE'  : 'django.db.backends.mysql', 
        'NAME'    : os.getenv('DB_NAME'     , 'appseed_db'),
        'USER'    : os.getenv('DB_USERNAME' , 'appseed_db_usr'),
        'PASSWORD': os.getenv('DB_PASS'     , 'pass'),
        'HOST'    : os.getenv('DB_HOST'     , 'localhost'),
        'PORT'    : os.getenv('DB_PORT'     , 3306),
        }, 
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'sdiarydos', 
            'USER': 'postgres', 
            'PASSWORD': 'Test@123',
            'HOST': '127.0.0.1', 
            'PORT': '5432',
        }
    }