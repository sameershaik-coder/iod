import locale
from django.contrib.auth.models import User
from apps.home.models import (
    UserProfile
)

def get_locale(user:User)->locale:
    user_profile = UserProfile.objects.get(user=user)
    country = user_profile.country
    if country == "IN":
        locale.setlocale(locale.LC_ALL, 'en_IN.UTF-8')
    else:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    return locale

        
        

    