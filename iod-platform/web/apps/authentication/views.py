# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm
from core.settings_templates.settings import GITHUB_AUTH
from apps.home.actions import networth as networth_actions, userprofile as userprofile_actions, user as user_actions
from django.contrib.auth.models import User
import logging
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordResetForm,SetPasswordForm
from django.contrib.auth.views import PasswordResetView
from apps.home.lib import user as user_lib
from django.contrib.auth import logout

# Get an instance of a logger
logger = logging.getLogger(__name__)

def logout_view(request):
    logout(request)
    return redirect('landing_page')

class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = None
            field.widget.attrs.update({'class': 'form-control'})

class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = None
            field.widget.attrs.update({'class': 'form-control'})

# views.py

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'accounts/registration/password_reset_form.html'  # Create this template as needed


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = None
            field.widget.attrs.update({'class': 'form-control'})
        
        

def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # To keep the user logged in
            new_password = form.cleaned_data.get("new_password1")
            logger.warning("Username : "+ user.email + " has successfully changed his old password")
            return redirect('password_change_done')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'accounts/change-password/change_password.html', {'form': form})

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data.get("email")
            logger.warning("-------------------------------------New user login with Username "+ email +" -------------------------------------")
            password = form.cleaned_data.get("password")
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("/app/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg, "GITHUB_AUTH": GITHUB_AUTH})


def register_user(request):
    """
    Registers a new user based on the provided request data.

    Parameters:
        request (HttpRequest): The HTTP request object containing the user registration data.

    Returns:
        HttpResponse: The HTTP response object containing the rendered registration page with the form, message, and success status.
    """
    msg = None
    success = False
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            result = user_lib.create_user(form.cleaned_data.get("email"),form.cleaned_data.get("email"),form.cleaned_data.get("password1"),form.cleaned_data.get('country'))
            if result:
                msg = 'User registration successful. Please click Sign In.'
                success = True
            else:
                msg = "User with provided email already exists. Please choose another email"

        else:
            msg = 'Provided data is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})
