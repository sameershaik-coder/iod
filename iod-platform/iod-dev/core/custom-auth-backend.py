# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        result = None
        try:
            user = UserModel.objects.filter(username=username).first()
            if user is None:
                result = UserModel.objects.get(email=username)
            else:
                if user.check_password(password):
                    result = user
        except UserModel.DoesNotExist:
                result = None
        return result
