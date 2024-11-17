from core.settings_templates.base import *
from core.settings_templates.database import *
import os
from dotenv import load_dotenv

#load env variables from env
load_dotenv()
ENV_SERVER = os.getenv('SERVER')
print("IP Address of the server is : " + str(ENV_SERVER))

USE_MOCK = False
print("USE_MOCK is set to : " + str(USE_MOCK))

#print("IP Address of the server is : " + str(env('SERVER')))

# load production server from .env
ALLOWED_HOSTS        = [str(ENV_SERVER),'172.28.179.215','localhost', 'localhost:85', '127.0.0.1',               env('SERVER', default='127.0.0.1') ]
CSRF_TRUSTED_ORIGINS = ['http://'+str(ENV_SERVER),'http://172.28.179.215/','http://localhost:85', 'http://127.0.0.1', 'https://' + env('SERVER', default='127.0.0.1') ]


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
            #'HOST': '127.0.0.1', 
            'HOST': '10.47.0.7',
            'PORT': '5432',
        }
    }