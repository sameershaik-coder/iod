# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("app/auth/", include("apps.authentication.urls")), # Auth routes - login / register
    path("app/configuration/", include("apps.configuration.urls")), 
    # UI pro app
    path("app/demo/", include("apps.demo.urls")),
    path("app/", include("apps.home.urls")),
    path('admin/', admin.site.urls),          # Django admin route
    # Leave `Home.Urls` as last the last line
    path("", include("apps.extsite.urls")),
    #path("", include("apps.esite.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)