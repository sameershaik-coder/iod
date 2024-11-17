import os
from dotenv import load_dotenv

#load env variables from env
load_dotenv()


# Get the value of the environment variable
#exec_env = os.environ.get('SDIARY_ENV', 'dev')
exec_env = os.getenv('SDIARY_ENV')
print("selected environment is : "+str(exec_env))

# Load the appropriate settings file based on the environment variable
if exec_env == 'prod':
    from core.settings_prod import *
elif exec_env == 'qa':
    from core.settings_qa import *
elif exec_env == 'uat':
    from core.settings_uat import *
elif exec_env == 'dev':
    from core.settings_dev import *
else:
    from core.settings_local import *




#############################################################
# OAuth settings 

GITHUB_ID     = os.getenv('GITHUB_ID', None)
GITHUB_SECRET = os.getenv('GITHUB_SECRET', None)
GITHUB_AUTH   = GITHUB_SECRET is not None and GITHUB_ID is not None

AUTHENTICATION_BACKENDS = (
    "core.custom-auth-backend.CustomBackend",
    #"allauth.account.auth_backends.AuthenticationBackend",
)

SITE_ID                    = 1 
ACCOUNT_EMAIL_VERIFICATION = 'none'

SOCIALACCOUNT_PROVIDERS = {}

if GITHUB_AUTH:
    SOCIALACCOUNT_PROVIDERS['github'] = {
        'APP': {
            'client_id': GITHUB_ID,
            'secret': GITHUB_SECRET,
            'key': ''
        }
    }