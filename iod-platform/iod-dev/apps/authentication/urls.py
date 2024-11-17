# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, include
from .views import login_view, register_user, change_password,logout_view
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from .views import CustomPasswordResetView,CustomSetPasswordForm

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", logout_view, name="logout"),
    #path('social_login/', include('allauth.urls')),
    #path('change-password/', auth_views.PasswordChangeView.as_view(template_name='accounts/change-password/change_password.html'), name='change_password'),
    path('change-password/', change_password, name='change_password'),
    path('change-password-done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/change-password/password_change_done.html'), name='password_change_done'),

    #forget password
    path('password_reset/', CustomPasswordResetView.as_view(), name='custom_password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/registration/password_reset_confirm.html',form_class=CustomSetPasswordForm), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/registration/password_reset_complete.html'), name='password_reset_complete'),
]
