# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [
    # path('email/', views.view_email, name='view_email'),
    # path('send-email/', views.send_email, name='send_email'),
    
    # upload pdf
    path('networth/upload', views.view_upload, name='view_upload'),
    # networth
    path('networth/backup/<int:backup_id>/restore', views.restore_backup, name='restore_backup'),
    path('networth/backup/<int:backup_id>/edit', views.edit_backup, name='edit_backup'),
    path('networth/backup/<int:backup_id>/delete', views.delete_backup, name='delete_backup'),
    path('networth/backup/add', views.create_backup, name='create_backup'),
    path('networth/backup/<int:backup_id>/restore', views.view_backups, name='restore_backup'),
    #path('restore/backup', views.view_backups, name='restore_now'),
    path('networth/backup', views.view_backups, name='view_backups'),
    path('nominee/send-email', views.send_email, name='send_nominee_email'),
    path('nominee/<int:pk>/delete', views.delete_nominee, name='delete_nominee'),
    path('nominee/<int:pk>/edit', views.edit_nominee, name='edit_nominee'),
    path('nominee/add', views.create_nominee, name='create_nominee'),
    path('nominee', views.view_nominee, name='view_nominee'),
    path('update_step_status/', views.update_step_status, name='update_step_status'),
    path("networth", views.networth, name="networth"),
    path("category/<int:pk>", views.category, name="category"),
    path("assets/<int:pk>", views.assets, name="assets"),
    # The home page
    path('', views.index, name='home'),
    path('profile', views.edit_user_profile_view, name='view_profile'),
    path('support',views.support, name="support"),
    path('settings',views.view_networth_settings, name="view_networth_settings"),
    path("networth/<int:networth_id>/edit", views.edit_networth_settings, name="edit_networth_settings"),
    #path('demo',views.demo, name="demo"),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
