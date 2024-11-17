import pytest
from tests.test_classes import BaseTest
from django.urls import reverse
from django.test import RequestFactory
from apps.configuration.models import(
    AssetType
)
from apps.home.models import(
    BaseUnit,
    Networth
)
from apps.configuration.views import (
    view_asset_types,
    create_asset_type,
    view_base_unit,
    create_base_unit,
)
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from apps.home.actions import(
    networth as networth_actions,
    baseunit as baseunit_actions,
    category as category_actions,
    assetgroup as ag_actions,
    instruments as instuments_actions,
    userprofile as up_actions,
)

def create_test_data_for_user(user):
    up_actions.do_create_user_profile(user,country="IN")
    networth = networth_actions.do_create_networth("Test Networth",32,user)
    baseunit = baseunit_actions.do_create_baseunit_with_user(user,networth)
    category = category_actions.do_create_category("Test Cat1",50,user)
    ag1 = ag_actions.do_create_assetgroup("Test AG1",50,category,acting_user=user)
    i1 = instuments_actions.do_create_instrument(name="sashjkas",weightage=10,amount_invested=10000,asset=ag1, acting_user=user,current_value=12000)
    i2 = instuments_actions.do_create_instrument(name="hdkahsdk",weightage=10,amount_invested=10000,asset=ag1, acting_user=user,current_value=13000)
    i3 = instuments_actions.do_create_instrument(name="sasiaosi",weightage=10,amount_invested=10000,asset=ag1, acting_user=user,current_value=7000)

def get_response_using_view_name(client, view_name):
    url = reverse(view_name)
    response = client.get(url)
    return response

def get_response_viewname_kwargs(client,view_name,kwargs):
    url = reverse(view_name ,kwargs=kwargs)
    response = client.get(url)
    return response

def post_response_using_view_name(client, view_name,data,user,param_set=None):
    url = reverse(view_name)
    if param_set is None:
        response = client.post(url, data=data,user=user)
        return response

def post_response_using_params(client, view_name,data,param_set):
    response = client.post(reverse(view_name, args=param_set), data=data)
    return response

def delete_response_using_params(client, view_name,param_set):
    response = client.delete(reverse(view_name, args=param_set))
    return response

################################################################################################################################
# Validation
################################################################################################################################

def validate_response(response, status,response_content_text,template_name=None):
    assert response.status_code == status
    assert response_content_text in response.content
    if template_name is not None :
        assert template_name in [template.name for template in response.templates]

def     assert_response_success(response, view_name):
    if view_name=="view_cas_upload":
        assert response.status_code == 200
        assert b'Upload CAS' in response.content
        assert "home/upload.html" in [template.name for template in response.templates]
    elif view_name=="view_base_unit":
        assert response.status_code == 200
        assert b'Base Unit Configuration' in response.content
        assert "home/configuration/base_unit.html" in [template.name for template in response.templates]
    elif view_name=="create_backup":
        assert response.status_code == 200
        assert b'InvestODiary -  Create Backup' in response.content
        assert "home/create_backup.html" in [template.name for template in response.templates]
    elif view_name=="view_backups":
        assert response.status_code == 200
        assert b'InvestODiary -  Backups Summary' in response.content
        assert "home/backups.html" in [template.name for template in response.templates]
    elif view_name=="networth":
        assert response.status_code == 200
        assert b'InvestODiary -  Networth Summary' in response.content
        assert "home/networth.html" in [template.name for template in response.templates]
    elif view_name == "category":
        assert response.status_code == 200
        assert b'InvestODiary -  Category Summary' in response.content
        assert "home/category.html" in [template.name for template in response.templates]
    elif view_name == "assets":
        assert response.status_code == 200
        assert b'InvestODiary -  Assets Summary' in response.content
        assert "home/assets.html" in [template.name for template in response.templates]
    elif view_name == "404":
        assert response.status_code == 200
        assert b'InvestODiary -  404 Page' in response.content
        assert "home/page-404.html" in [template.name for template in response.templates]
    elif view_name == "500":
        assert response.status_code == 200
        assert b'InvestODiary -  500 Page' in response.content
        assert "home/page-500.html" in [template.name for template in response.templates]
    elif view_name == "301":
        assert response.status_code == 301
        assert b'' in response.content
        #assert "home/page-404.html" in [template.name for template in response.templates]
    elif view_name == "support":
        assert response.status_code == 200
        assert b'InvestODiary -  Support' in response.content
        assert "home/support.html" in [template.name for template in response.templates]    
    elif view_name == "demo":
        assert response.status_code == 200
        assert b'InvestODiary -  404 Page' in response.content
        assert "home/page-404.html" in [template.name for template in response.templates]    
    elif view_name=="view_profile":
        assert response.status_code == 200
        assert b'InvestODiary -  Profile' in response.content
        assert "home/edit_profile.html" in [template.name for template in response.templates]
    elif view_name=="settings":
        assert response.status_code == 200
        assert b'InvestODiary -  Settings' in response.content
        assert "home/networth_settings.html" in [template.name for template in response.templates]

def assert_data_in_context(response,data):
    for item in data:
        assert item in response.context

def assert_data_not_in_context(response,data):
    for item in data:
        assert item not in response.context

def assert_response_redirect(response, view_name):
    if view_name=="view_asset_types":   
        assert response.status_code == 302
        assert response.url == reverse(view_name)
        assert response.content == b''
        assert response.templates == []
    if view_name=="login":
        assert response.status_code == 302
        assert response.url == '/admin/login/?next=/admin/'
        assert response.content == b''
        assert response.templates == []
    if view_name=="view_profile":
        assert response.status_code == 302
        assert response.url == reverse(view_name)
        assert response.content == b''
        assert response.templates == []

#def validate_response_context(response, status,response_content_text,template_name=None):