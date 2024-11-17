from django.urls import path, re_path
from apps.demo import views

urlpatterns = [
    path("pages/index", views.demo, name="demo"),
    re_path(r'^.*\.*', views.pages, name='pages'),
    
]