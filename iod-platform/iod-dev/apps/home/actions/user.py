from apps.home.models import UserProfile
from django.contrib.auth.models import User
from typing import Optional
from apps.home.actions import(
    networth as networth_actions,
    userprofile as userprofile_actions,
    usertour as usertour_actions
)
from django.db import transaction

def get_user_by_email(email: str) -> User:
    return User.objects.get(email = email)

def do_create_user(
    username: Optional[str] = None,
    password: Optional[str] = None,
    country: Optional[str] = None,
    email: Optional[str] = None,
    bio: Optional[str] = None,
) -> User:
    with transaction.atomic():
        user = User.objects.create_user(
            username = username,
            password = password,
            email = email
        )
        userprofile_actions.do_create_user_profile(user=user,country=country)
        networth_actions.do_create_networth(username.split('@')[0]+ " Networth",1,user)
        usertour_actions.do_create_user_tour_for_new_user(user=user)
    return user

