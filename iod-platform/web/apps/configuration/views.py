from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import(
   AssetType,
   
)
from apps.home.models import(
    Networth,
)
from apps.home.actions import baseunit as baseunit_action, assettype as assettype_actions
from .forms import AssetTypeForm,BaseUnitForm,NetworthForm
from django.shortcuts import render, redirect
from apps.configuration.lib import (
    networth as networth_lib,
    assetgroup as ag_common,
    baseunit as bu_common,
    category as category_lib,
    instruments as instrument_lib
)
import logging
from apps.common import pages as pages_common

# Get an instance of a logger
logger = logging.getLogger(__name__)

@login_required(login_url="/login/")
def create_instrument(request,category_id,asset_group_id):
    try:
        if request.method == 'POST':
            return instrument_lib.fetch_post_response_instrument_add(request, category_id,asset_group_id)
        else:
            return instrument_lib.fetch_get_response_instrument_add(request, category_id,asset_group_id)
    except Exception as e:
        return pages_common.render_404_page(context={}, request=request, exception=e)


@login_required(login_url="/login/")
def delete_instrument(request, category_id,asset_group_id,instrument_id):
    try:
        return instrument_lib.fetch_get_response_delete(request, instrument_id, asset_group_id, category_id)
    except Exception as e:
        return pages_common.render_404_page(context={}, request=request, exception=e)

@login_required(login_url="/login/")
def edit_instrument(request,category_id, asset_group_id, instrument_id):
    try:
        if request.method == 'POST':
            return instrument_lib.fetch_post_response_instrument_edit(request,category_id,asset_group_id,instrument_id)
        else:
            return instrument_lib.fetch_get_response_instrument_edit(request, instrument_id)
    except Exception as e:
        return pages_common.render_404_page(context={}, request=request, exception=e)

@login_required(login_url="/login/")
def view_instruments(request, category_id,asset_group_id):
    try:
        return instrument_lib.fetch_get_response_instruments_view(request,category_id,asset_group_id)
    except:
        return pages_common.render_404_page(context={}, request=request)

@login_required(login_url="/login/")
def create_asset_group(request,category_id):
    try:
        context = {}
        if request.method == 'POST':
            return ag_common.fetch_post_response_create(request, context, category_id)
        else:
            return ag_common.handle_get_asset_group(request, context, category_id)
    except Exception as e:
        return pages_common.render_404_page(context={}, request=request,exception=e)


@login_required(login_url="/login/")
def delete_asset_group(request, asset_group_id,category_id):
    try:
        return ag_common.fetch_get_response_delete(request, category_id, asset_group_id)
    except Exception as e:
       return pages_common.render_404_page(context={}, request=request, exception=e)
    

@login_required(login_url="/login/")
def edit_asset_group(request, asset_group_id,category_id):
    try:
        context = {}
        if request.method == 'POST':
            return ag_common.fetch_post_response_edit_asset_group(request, context, category_id, asset_group_id)
        else:
            return ag_common.fetch_get_response_edit_asset_group(request, context, category_id, asset_group_id)
    except Exception as e:
        return pages_common.render_404_page(context={}, request=request, exception=e)

@login_required(login_url="/login/")
def view_asset_groups(request, category_id=None):
    """
    Retrieves the asset group view context based on the category ID provided.
    Returns the asset group view context.
    If an exception occurs, renders a 404 page.
    """
    try:
        return ag_common.get_asset_group_view_context(request, category_id)
    except:
        return pages_common.render_404_page(context={}, request=request)

@login_required(login_url="/login/")
def delete_category(request, category_id):
    """
    Deletes a category with the given category_id after checking user ownership and category validity. 
    Redirects to 'view_networth' after successful deletion. 
    In case of an exception, logs the error and redirects to 'view_networth'. 
    """
    try:
        return category_lib.fetch_get_response_delete_category(request, category_id)
    except Exception as e:
        return pages_common.render_404_page(context={}, request=request, exception=e)

@login_required(login_url="/login/")
def create_category(request):
    """
    A view function to create a new category based on user input.
    
    Parameters:
    - request: HttpRequest object containing metadata about the request
       
    Returns:
    - Rendered HTML template displaying the form to create a new category
    """
    context={}
    try:
        if request.method == 'POST':
            return category_lib.fetch_post_response_create_category(request, context)
        else:
            return category_lib.fetch_get_response_create_category(request, context)
    except Exception as e:
        return pages_common.render_404_page(context={}, request=request, exception=e)
    
@login_required(login_url="/login/")
def edit_category(request, category_id):
    """
    View to edit a category, updating its name and weightage based on user input.
    
    Parameters:
    - request: HttpRequest object
    - category_id: int, the id of the category to be edited
    
    Returns:
    - HttpResponse object
    """
    context={}
    try:
        if request.method == 'POST':
            return category_lib.fetch_post_response_edit_category(request, context, category_id)
        else:
            return category_lib.fetch_get_response_edit_category(request, context, category_id)
    except Exception as e:
        return pages_common.render_404_page(context={}, request=request, exception=e)
    
# below not in use
@login_required(login_url="/login/")
def edit_networth(request, networth_id):
    networth = Networth.objects.get(id=networth_id)
    context = {}
    if request.method == 'POST':
        form = NetworthForm(request.POST)
        if form.is_valid():
            networth.name = form.cleaned_data['name']
            networth.amount = form.cleaned_data['amount']
            
            networth.save()
            return redirect('view_networth')
        else:
            context['form'] = form
            context['is_edit'] = True
    else:
        form = NetworthForm(initial={
            'name': networth.name,
            'amount': networth.amount
        })

        context = {
            'form': form,
            'is_edit': True,    
            'networth': networth
        }
    context['segment'] = ['settings']
    html_template = loader.get_template('home/configuration/networth_settings.html')
    return HttpResponse(html_template.render(context, request))

# below method is view networth configuration which should not be confused with networth settings
@login_required(login_url="/login/")
def view_networth(request):
    """
    View function for displaying the networth configuration of a user.

    Parameters:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: The HTTP response object containing the rendered template.
    Raises:
        ObjectDoesNotExist: If the net worth object does not exist for the user.
    """
    context = {}
    try:
        return networth_lib.fetch_get_response_view_networth(context,request)
    except Exception as e:
        return pages_common.render_404_page(context={}, request=request, exception=e)

# below not in use
@login_required(login_url="/login/")
def create_base_unit(request):
    context={}
    if request.method == 'POST':
        form = BaseUnitForm(request.POST)
        if form.is_valid():
            try:
                name = form.cleaned_data.get("name")
                value = form.cleaned_data.get("value")
                user = request.user
                networth = Networth.objects.get(user=user)
                baseunit_action.do_create_baseunit(name,value,networth)
                return redirect('view_base_unit')
            except:
                form = BaseUnitForm()
                context["form"] = form
                context['error_message'] = 'Invalid form. Please correct the errors below.' 
    else:
        form = BaseUnitForm()
        context["form"] = form
    return render(request, 'home/configuration/create_base_unit.html', context)

@login_required(login_url="/login/")
def edit_base_unit(request, base_unit_id):
    """
    Edit the base unit with the given base_unit_id.

    Parameters:
        request (HttpRequest): The HTTP request object.
        base_unit_id (int): The ID of the base unit to be edited.

    Returns:
        HttpResponse: The HTTP response object. If the request method is POST and the form is valid, it redirects to 'view_base_unit'. 
        Otherwise, it renders the 'base_unit.html' template with the form, is_edit flag, and the base_unit object.
    """
    context={} 
    try:
        if request.method == 'POST':
            return bu_common.fetch_post_response_edit_baseunit(request, base_unit_id)
        else:
            return bu_common.handle_edit_baseunit_get(request, base_unit_id)
    except Exception as e:
        return pages_common.render_404_page(context=context, request=request, exception=e)

@login_required(login_url="/login/")
def view_base_unit(request):
    """
    View for the base unit, requires login. Retrieves base units for the logged-in user and renders the 'base_unit.html' template.
    Parameters:
    - request: the HTTP request object
    Returns:
    - HttpResponse object
    """
    context={} 
    try:
        response, context = bu_common.handle_view_baseunit(context,request)
        return response
    except Exception as e:
        return pages_common.render_404_page(context=context, request=request, exception=e) 

# below all asset type methods are not in use
@login_required(login_url="/login/")
def view_asset_types(request,pk=None):
    context={} 
    user_email = request.user.email
    logged_user = get_object_or_404(User,email = user_email)
    if request.method == 'GET':
        try:
            networth = Networth.objects.get(user = logged_user,is_active = True)
            asset_types_list = AssetType.objects.filter(networth = networth)
            context["asset_types_list"] = asset_types_list
        except:
            html_template = loader.get_template('home/page-404.html')
            return HttpResponse(html_template.render(context, request))

    html_template = loader.get_template('home/configuration/asset_types.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def create_asset_type(request):
    context = {}
    if request.method == 'POST':
        form = AssetTypeForm(request.POST)
        if form.is_valid():
            try:
                name = form.cleaned_data.get("name")
                weightage = form.cleaned_data.get("weightage")
                assettype_actions.do_create_assettype(name, weightage, request.user)
                return redirect('view_asset_types')
            except:
                context['error_message'] = 'Invalid data. Unable to create the asset type with provided input'
        else:
            context['form'] = form  # Pass the form instance with errors back to the template
    else:
        form = AssetTypeForm()
        context['form'] = form
    return render(request, 'home/configuration/create_asset_type.html', context)



@login_required(login_url="/login/")
def edit_asset_type(request, asset_type_id):
    asset_type = AssetType.objects.get(id=asset_type_id)
    context={}
    if request.method == 'POST':
        print("inside POST of edit asset type")
        form = AssetTypeForm(request.POST)
        if form.is_valid():
            print("form is valid")
            asset_type.name = form.cleaned_data['name']
            asset_type.weightage = form.cleaned_data['weightage']
            asset_type.save()
            return redirect('view_asset_types')
        else:
            context['form'] = form 
            context['is_edit'] = True
    else:
        print("inside GET of edit asset type")
        form = AssetTypeForm(initial={
            'name': asset_type.name,
            'weightage': asset_type.weightage
        })

        context = {
            'form': form,
            'is_edit': True,
            'asset_type' : asset_type
        }
    html_template = loader.get_template('home/configuration/asset_types.html')
    return HttpResponse(html_template.render(context, request))

def delete_asset_type(request, asset_type_id):
    asset_type = get_object_or_404(AssetType, id=asset_type_id)
    asset_type.delete()
    return redirect('view_asset_types')