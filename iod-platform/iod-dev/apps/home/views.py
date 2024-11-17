# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from apps.home.lib import (
    email, 
    userprofile as userprofile_lib,
    nominee as nominee_lib,
    )
from .lib import (
    networth_summary as networth_summary_lib,
    category_summary as category_summary_lib,
    assets_summary as assets_summary_lib,
    usertour as usertour_lib,
    backups as backups_lib,
    upload_cas as upload_cas_lib
)
from apps.home.lib import networth_settings as nw_settings
from apps.common import pages as pages_common
from apps.home.forms import PDFDocumentForm
from django.shortcuts import render, redirect
from django.http import HttpResponse


def view_upload(request):
    try:
        if request.method == 'POST':
            return upload_cas_lib.fetch_post_response_edit(request)
        else:
            return upload_cas_lib.fetch_get_response_edit(request)
    except Exception as e:
        return pages_common.render_error_page(context={}, request=request, exception=e)
def restore_backup(request,backup_id):
    try:
        return backups_lib.fetch_post_response_restore(request,backup_id)
    except Exception as e:
        return pages_common.render_error_page(context={}, request=request, exception=e)

def edit_backup(request,backup_id):
    try:
        if request.method == 'POST':
            return backups_lib.fetch_post_response_edit(request,backup_id)
        else:
            return backups_lib.fetch_get_response_edit(request,backup_id)
    except Exception as e:
        return pages_common.render_error_page(context={}, request=request, exception=e)

def delete_backup(request,backup_id):
    try:
        return backups_lib.fetch_post_response_delete(request,backup_id)
    except Exception as e:
        return pages_common.render_error_page(context={}, request=request, exception=e)
    
@login_required(login_url="/login/")
def create_backup(request):
    if request.method == 'POST':
        return backups_lib.fetch_post_response_add(request)
    else:
        return backups_lib.fetch_get_response_add(request)

@login_required(login_url="/login/")
def view_backups(request):
    try:
        return backups_lib.fetch_get_response_view(request)
    except Exception as e:
        return pages_common.render_error_page(context={}, request=request, exception=e)
    
def send_email(request):
    try:
        return email.fetch_post_response_send(request)
    except Exception as e:
        return pages_common.render_error_page(context={}, request=request, exception=e)

@login_required(login_url="/login/")
def delete_nominee(request, pk): 
    try:
        return nominee_lib.fetch_post_response_delete(request)
    except Exception as e:
        return pages_common.render_error_page(context={}, request=request, exception=e)

@login_required(login_url="/login/")
def edit_nominee(request, pk):
    # pk is not in use currently, might be used in future
    try:
        if request.method == 'POST':
            return nominee_lib.fetch_post_response_edit(request)
        else:
            return nominee_lib.fetch_get_response_edit(request)
    except Exception as e:
        return pages_common.render_error_page(context={}, request=request, exception=e)

@login_required(login_url="/login/")
def create_nominee(request):
    try:
        if request.method == 'POST':
            return nominee_lib.fetch_post_response_add(request)
        else:
            return nominee_lib.fetch_get_response_add(request)
    except Exception as e:
        return pages_common.render_error_page(context={}, request=request, exception=e)
    
@login_required(login_url="/login/")
def view_nominee(request, pk=None):
    try:
        return nominee_lib.fetch_get_response_view(request)
    except Exception as e:
        return pages_common.render_error_page(context={}, request=request, exception=e)

def update_step_status(request):
    return usertour_lib.fetch_post_response_user_tour_step(request)

@login_required(login_url="/login/")
def edit_networth_settings(request, networth_id=int):
    try:
        # networth_id might be used in future, currently one user will have only one networth so not used
        if request.method == 'POST':
            return nw_settings.fetch_post_response_edit(request)
        else:
            return nw_settings.fetch_get_response_edit(request)
    except Exception as e:
        return pages_common.render_error_page(context={}, request=request, exception=e)

@login_required(login_url="/login/")
def view_networth_settings(request):
    try:
        return nw_settings.fetch_get_response_view(request)
    except Exception as e:
        return pages_common.render_error_page(context={}, request=request, exception=e)

@login_required(login_url="/login/")
def assets(request,pk:int):
    try:
        return assets_summary_lib.fetch_get_response_view(request,pk)
    except Exception as e:
        return pages_common.render_error_page(context={}, request=request, exception=e)

@login_required(login_url="/login/")
def category(request,pk:int):
    try:
        return category_summary_lib.fetch_get_response_view(request,pk)
    except Exception as e:
        return pages_common.render_error_page(context={}, request=request, exception=e)

@login_required(login_url="/login/")
def networth(request):
    try:
        return networth_summary_lib.fetch_get_response_view(request)
    except Exception as e:
        return pages_common.render_error_page(context={}, request=request, exception=e)


@login_required(login_url="/login/")
def edit_user_profile_view(request):
    try:
        if request.method == 'POST':
            return userprofile_lib.fetch_post_response_edit(request)
        else:
            return userprofile_lib.fetch_get_response_edit(request)
    except Exception as e:
       return pages_common.render_error_page(context={}, request=request, exception=e)
    
@login_required(login_url="/login/")
def index(request):
    # context = {'segment': 'index'}

    # html_template = loader.get_template('home/index-options.html')
    # return HttpResponse(html_template.render(context, request))
    return HttpResponseRedirect(reverse('networth')) 

@login_required(login_url="/login/")
def support(request):
    context = {'segment': 'support'}

    html_template = loader.get_template('home/support.html')
    return HttpResponse(html_template.render(context, request))

# @login_required(login_url="/login/")
# def demo(request):
#     context = {'segment': 'demo'}

#     html_template = loader.get_template('home/index-options.html')
#     return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
