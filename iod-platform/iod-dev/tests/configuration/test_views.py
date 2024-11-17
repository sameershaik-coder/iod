import pytest
from apps.home.lib.exceptions import JsonableError
from tests.test_classes import BaseTest
from django.urls import reverse
from django.test import RequestFactory
from apps.configuration.models import(
    AssetType,
    
)
from apps.home.models import(
    BaseUnit,
    Networth,
    Category,
    AssetGroup,
    Instrument,
    UserTour,
    UserTourStep
)
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from test_common import (
    get_response_using_view_name,
    get_response_viewname_kwargs,
    post_response_using_view_name,
    post_response_using_params,
    delete_response_using_params,
    validate_response,
    assert_response_redirect,
    assert_response_success
)
from common.test_data.asset_type import (
    get_default_asset_type_data,
    set_default_asset_type_data,
    assert_asset_type,
)
from common.test_data.base_unit import (
    set_default_base_unit_data,
    get_default_base_unit_data,
    assert_base_unit_default,
    assert_base_unit
)
from common.test_data import networth as networth_test_data
from common.test_data import category as category_test_data
from common.test_data import asset_group as asset_group_test_data
from common.test_data import instrument as instrument_test_data
from unittest.mock import patch

################################################################################################################################
# update step status API
################################################################################################################################
class Test_UpdateTourSteps_Views(BaseTest):
    def test_view_update_step_status_post(self,user,client):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        user_tour = UserTour.objects.get(user=user)
        step = UserTourStep.objects.get(tour=user_tour, step_name="1")
        response = client.post(reverse('update_step_status'), {'name': '1', 'status': 'Completed'}, content_type='application/json')
        assert response.status_code == 200
        assert response.json() == {'status': 'success'}
        step.refresh_from_db()
        assert step.status =='Completed'
        user_tour.refresh_from_db()
        assert user_tour.status == 'In-Progress'
    
    def test_update_step_status_get(self,user,client):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        response = client.get(reverse('update_step_status'))
        assert response.status_code == 200
        assert response.json() == {'status': 'failed'}

################################################################################################################################
# Asset-Group Configuration
################################################################################################################################

@pytest.mark.django_db
class Test_Instrument_Views(BaseTest):
    
    def test_view_instrument_group_http404(self,client,category,assetgroup):
        other_user = User.objects.create_user(username='other_user', password='password')
        self.user_login(client, other_user)
        response = get_response_viewname_kwargs(client,"view_instruments",kwargs={'category_id': category.id
                                                                                   ,'asset_group_id' : assetgroup.id})
        
        validate_response(response,200,b'InvestODiary -  404 Page','home/page-404.html')

    def test_view_instruments(self,user,client,networth,category,assetgroup):
            self.initialize_user(user,False,False,True)
            self.user_login(client,user)
            # # Create some test data
            i1 = Instrument.objects.create(name='Test AG 1', amount_invested=10, asset=assetgroup)
            i2 = Instrument.objects.create(name='Test Ag 2', amount_invested=20, asset=assetgroup)
            
            response = get_response_viewname_kwargs(client,"view_instruments",kwargs={'category_id': category.id,
                                                                                      'asset_group_id' : assetgroup.id})
            
            # Check that the response contains the asset type names
            assert i1.name in str(response.content)
            assert i2.name in str(response.content)
            
            # Check that the response status code is 200
            assert response.status_code == 200

    def test_edit_instrument_view_raise_exception(self, user,client, category,assetgroup,instrument):
        other_user = User.objects.create_user(username='other_user', password='password')
        self.user_login(client,other_user)
        other_user.email = user.email
        other_user.save()

        data = instrument_test_data.get_default_instrument_data()

        response = post_response_using_params(client,"edit_instrument",data,[category.id,assetgroup.id,instrument.id])
        assert_response_success(response,"404")

    def test_edit_instrument_view_invalid_data(self, user,client, category,assetgroup,instrument):
        
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)
       
        # Make a GET request to the edit category page
        response = client.get(reverse("edit_instrument", kwargs={'category_id': category.id, 
                                                                  'asset_group_id':assetgroup.id,
                                                                  'instrument_id' : instrument.id}))

        # Check that the response status code is 200
        assert response.status_code == 200

        # Make a POST request to update the category
        updated_name = "@$%"
        updated_amount_invested = -1
        updated_current_value = -1
        data = instrument_test_data.set_default_instrument_data(updated_name,updated_amount_invested,updated_current_value)

        response = post_response_using_params(client,"edit_instrument",data,[category.id,assetgroup.id,instrument.id])
        validate_response(response,200,b'InvestODiary -  Configuration - Asset-Group','home/configuration/asset-group.html')
        assert 'form' in response.context
        form_errors = response.context["form"].errors
        assert form_errors["amount_invested"][0] == "Amount Invested must be greater than zero."
        assert form_errors["current_value"][0] == "Current Value must be greater than zero."
        assert form_errors["name"][0] == "Instrument Name must contain only letters, numbers, underscores or hyphens."

    def test_edit_instrument_view(self, user,client, category,assetgroup,instrument):
         
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)
       
        # Make a GET request to the edit category page
        response = client.get(reverse("edit_instrument", kwargs={'category_id': category.id, 
                                                                  'asset_group_id':assetgroup.id,
                                                                  'instrument_id' : instrument.id}))

        # Check that the response status code is 200
        assert response.status_code == 200

        # Make a POST request to update the category
        updated_name = "New instrument Name"
        updated_amount_invested = 50000
        updated_current_value = 60000

        data = instrument_test_data.set_default_instrument_data(updated_name,updated_amount_invested,updated_current_value)
        response = post_response_using_params(client,"edit_instrument",data,[category.id,assetgroup.id,instrument.id])

        # Check that the response status code is a redirect (302)
        assert response.status_code == 302

        # Check that the asset type was updated
        instrument.refresh_from_db()
        instrument_test_data.assert_instrument(instrument,assetgroup,data)

        # Make a POST request to update the category
        updated_name = "New instrument Name"
        updated_amount_invested = 50000
        updated_current_value = 40000

        data = instrument_test_data.set_default_instrument_data(updated_name,updated_amount_invested,updated_current_value)
        response = post_response_using_params(client,"edit_instrument",data,[category.id,assetgroup.id,instrument.id])

        # Check that the response status code is a redirect (302)
        assert response.status_code == 302

        # Check that the asset type was updated
        instrument.refresh_from_db()
        instrument_test_data.assert_instrument(instrument,assetgroup,data)

    def test_delete_instrument(self,user,client,category,assetgroup,instrument):

        # create a user and log in
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)

        # send a delete request to the view with the asset type id
        response = delete_response_using_params(client,'delete_instrument',[category.id,assetgroup.id,instrument.id])

        # check that the response status code is 302 (redirect)
        assert response.status_code == 302

        # check that the asset type is deleted
        assert not Instrument.objects.filter(id=instrument.id).exists()        

    def test_delete_instrument_invalid_user(self,user,client,category,assetgroup,instrument):
        other_user = User.objects.create_user(username='other_user', password='password')
        self.user_login(client, other_user)

        # send a delete request to the view with the asset type id
        response = delete_response_using_params(client,'delete_instrument',[category.id,assetgroup.id,instrument.id])
        
        assert_response_success(response,"404")

    def test_create_instrument_invalid_raise_exception(self,user,client,category,assetgroup,instrument):
        other_user = User.objects.create_user(username='other_user', password='password')
        self.user_login(client,other_user)
        other_user.email = user.email
        other_user.save()

        data = {
            'name': 'New Instrumentsasasasas',
            'amount_invested': 10,
            'current_value' : 10
        }

        response = post_response_using_params(client,"create_instrument",data,[category.id,assetgroup.id])
        assert_response_success(response,"404")

    def test_create_instrument_invalid_bad_form_data(self,user,client,category,assetgroup,instrument):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        data = {
            'name': '$&^%#@',
            'amount_invested': -10,
            'current_value' : -1
        }
        response = post_response_using_params(client,"create_instrument",data,[category.id,assetgroup.id])

        validate_response(response,200,b'Add a new Instrument','home/configuration/create_instrument.html')

        assert 'form' in response.context
        form_errors = response.context["form"].errors
        assert form_errors["amount_invested"][0] == "Amount Invested must be greater than zero."
        assert form_errors["name"][0] == "Instrument Name must contain only letters, numbers, underscores or hyphens."

        # try creating a category with name same as existing category name
        data = {
            'name': instrument.name,
            'amount_invested': 10,
            'current_value' : 10
        }
        
        response = post_response_using_params(client,"create_instrument",data,[category.id,assetgroup.id])
        assert 'form' in response.context
        error_message = response.context["error_message"]
        assert error_message == "Instrument already exists with name : " + instrument.name
    
    def test_create_instrument(self,client,user,category,assetgroup):
        self.initialize_user(user,False,False,True)
        data = instrument_test_data.get_default_instrument_data()
        self.user_login(client,user)
        response = post_response_using_params(client,"create_instrument",data,[category.id,assetgroup.id])

        assert_response_redirect(response,"view_instruments")
        i1 = Instrument.objects.get(name=data['name'])
        instrument_test_data.assert_instrument(i1,assetgroup,data)

    def test_create_instrument_get(self,client,user,category,assetgroup):
        self.initialize_user(user,False,False,True)
        data = instrument_test_data.get_default_instrument_data()
        self.user_login(client,user)
        response = get_response_viewname_kwargs(client,"create_instrument",kwargs={'category_id': category.id,'asset_group_id': assetgroup.id})
        
        assert response.status_code == 200
        validate_response(response,200,b'InvestODiary -  Add Instrument','home/configuration/create_instrument.html')

@pytest.mark.django_db
class Test_AssetGroups_Views(BaseTest):
    
    def test_view_asset_group_http404(self,client,category):
        other_user = User.objects.create_user(username='other_user', password='password')
        self.user_login(client, other_user)
        response = get_response_viewname_kwargs(client,"view_asset_groups",kwargs={'category_id': category.id})
        
        validate_response(response,200,b'InvestODiary -  404 Page','home/page-404.html')
    
    def test_view_asset_groups(self,user,client,networth,category):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        # # Create some test data
        ag_1 = AssetGroup.objects.create(name='Test AG 1', weightage=10, category=category)
        ag_2 = AssetGroup.objects.create(name='Test Ag 2', weightage=20, category=category)
        
        response = get_response_viewname_kwargs(client,"view_asset_groups",kwargs={'category_id': category.id})
        
        # Check that the response contains the asset type names
        assert ag_1.name in str(response.content)
        assert ag_2.name in str(response.content)
        
        # Check that the response status code is 200
        assert response.status_code == 200

    def test_view_asset_groups_invalid_post_request(self,user,client,networth,category):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        # # Create some test data
        ag_1 = AssetGroup.objects.create(name='Test AG 1', weightage=10, category=category)
        ag_2 = AssetGroup.objects.create(name='Test Ag 2', weightage=20, category=category)
        
        response = get_response_viewname_kwargs(client,"view_asset_groups",kwargs={'category_id': category.id})
        
        # Check that the response contains the asset type names
        assert ag_1.name in str(response.content)
        assert ag_2.name in str(response.content)
        
        # Check that the response status code is 200
        assert response.status_code == 200

    def test_view_asset_groups_fully_allocated(self,user,client,category):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        # # Create some test data
        ag_1 = AssetGroup.objects.create(name='Test AG 1', weightage=10, category=category)
        ag_2 = AssetGroup.objects.create(name='Test Ag 2', weightage=20, category=category)
        
        response = client.post(reverse("view_asset_groups",kwargs={'category_id': category.id}))
        assert_response_success(response,"404")
        
    
    def test_edit_asset_group_invalid_existing_name(self, user,client, category,assetgroup):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        ag_1 = AssetGroup.objects.create(name='Test AG 2', weightage=10, category=category)

        # Make a POST request to update the asset with another asset name
        updated_name = "Test AG 2"
        updated_weightage = 10
        data = asset_group_test_data.set_default_asset_group_data(updated_name,updated_weightage)

        # Make a POST request to the edit category page
        response = post_response_using_params(client,"edit_asset_group",data,[category.id,assetgroup.id])
        error_messsage = response.context["error_message"]
        assert error_messsage == f'Asset group with name {updated_name} already exists'

    def test_edit_asset_group_view_raise_exception(self, user,client, category,assetgroup):
        
        other_user = User.objects.create_user(username='other_user', password='password')
        self.user_login(client,other_user)
        other_user.email = user.email
        other_user.save()
       
        # Make a POST request to update the category
        updated_name = "sample"
        updated_weightage = 10
        data = asset_group_test_data.set_default_asset_group_data(updated_name,updated_weightage)

        # Make a POST request to the edit category page
        response = post_response_using_params(client,"edit_asset_group",data,[category.id,assetgroup.id])
        assert_response_success(response,"404")


    def test_edit_asset_group_view_invalid_data(self, user,client, category,assetgroup):
        
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)
       
        # Make a GET request to the edit category page
        response = client.get(reverse("edit_asset_group", kwargs={'category_id': category.id, 'asset_group_id':assetgroup.id}))

        # Check that the response status code is 200
        assert response.status_code == 200

        # Make a POST request to update the category
        updated_name = "@$%"
        updated_weightage = -1
        data = asset_group_test_data.set_default_asset_group_data(updated_name,updated_weightage)

        response = post_response_using_params(client,"edit_asset_group",data,[category.id,assetgroup.id])
        validate_response(response,200,b'InvestODiary -  Configuration - Category','home/configuration/category.html')
        assert 'form' in response.context
        form_errors = response.context["form"].errors
        assert form_errors["weightage"][0] == "Weightage must be greater than zero."
        assert form_errors["name"][0] == "Asset-Group Name must contain only letters, numbers, underscores or hyphens."

        weightage_used = category.get_total_weightage_used() 

        previous_ag_weightage = assetgroup.weightage 
        available_weightage = 100 - weightage_used + previous_ag_weightage 
        over_weightage = available_weightage+1
        #updated_weightage_sum = weightage_used + category.weightage - previous_cat_weightage 

        # Make a POST request to update the category
        updated_name = "updated asset group new"
        updated_weightage = over_weightage
        data = asset_group_test_data.set_default_asset_group_data(updated_name,updated_weightage)

        response = post_response_using_params(client,"edit_asset_group",data,[category.id,assetgroup.id])

        validate_response(response,200,b'InvestODiary -  Configuration - Category','home/configuration/category.html')
        error_messsage = response.context["error_message"]
        assert error_messsage =='Invalid weightage. Weightage should be equal to or less than ' + str(available_weightage ) 
        
    
    def test_edit_category_view_raise_exception(self, user,client,category):
         
        other_user = User.objects.create_user(username='other_user', password='password')
        self.user_login(client,other_user)
        other_user.email = user.email
        other_user.save()

        # Make a POST request to update the category
        updated_name = "New Cat Name"
        updated_weightage = 50

        data = category_test_data.set_default_category_data(updated_name,updated_weightage)

        response = post_response_using_params(client,"edit_category",data,[category.id])
        assert_response_success(response,"404")

    def test_edit_category_view(self, user,client,networth, category,assetgroup):
         
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)
       
        # Make a GET request to the edit category page
        response = client.get(reverse("edit_asset_group", args=[category.id,assetgroup.id]))

        # Check that the response status code is 200
        assert response.status_code == 200

        # Make a POST request to update the category
        updated_name = "New AssetGroup Name"
        updated_weightage = 50

        data = asset_group_test_data.set_default_asset_group_data(updated_name,updated_weightage)
        response = post_response_using_params(client,"edit_asset_group",data,[category.id,assetgroup.id])

        # Check that the response status code is a redirect (302)
        assert response.status_code == 302

        # Check that the asset type was updated
        assetgroup.refresh_from_db()
        asset_group_test_data.assert_asset_group(assetgroup,data,category)

    def test_delete_category(self,user,client,category,assetgroup):

        # create a user and log in
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)

        # send a delete request to the view with the asset type id
        response = delete_response_using_params(client,'delete_asset_group',[category.id,assetgroup.id])

        # check that the response status code is 302 (redirect)
        assert response.status_code == 302

        # check that the asset type is deleted
        assert not AssetGroup.objects.filter(id=assetgroup.id).exists()    
    
    def test_delete_asset_group_invalid_raise_exception(self,user,client,category,assetgroup):
        other_user = User.objects.create_user(username='other_user', password='password')
        self.user_login(client,other_user)
        other_user.email = user.email
        other_user.save()

        # send a delete request to the view with the asset type id
        response = delete_response_using_params(client,'delete_asset_group',[category.id,assetgroup.id])
        assert_response_success(response,"404")




    def test_asset_group_category_invalid_bad_form_data(self,user,client,category,assetgroup):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        data = {
            'name': '$&^%#@',
            'weightage': -10
        }
        response = post_response_using_params(client,"create_asset_group",data,[category.id])

        validate_response(response,200,b'Add a new Asset-Group','home/configuration/create_asset_group.html')

        assert 'form' in response.context
        form_errors = response.context["form"].errors
        assert form_errors["weightage"][0] == "Weightage must be greater than zero."
        assert form_errors["name"][0] == "Asset-Group Name must contain only letters, numbers, underscores or hyphens."

        weightage_used = category.get_total_weightage_used() 
        available_weightage = 100 - weightage_used 

        over_weightage = available_weightage + 1

        data = {
            'name': 'some asset-group',
            'weightage': over_weightage
        }
        response = post_response_using_params(client,"create_asset_group",data,[category.id])

        validate_response(response,200,b'Add a new Asset-Group','home/configuration/create_asset_group.html')

        error_messsage = response.context["error_message"]
        assert error_messsage =='Invalid weightage. Weightage should be equal to or less than ' + str(available_weightage ) 

        # try creating a category with name same as existing category name
        data = {
            'name': assetgroup.name,
            'weightage': 10
        }
        response = post_response_using_params(client,"create_asset_group",data,[category.id])
        error_messsage = response.context["error_message"]
        assert error_messsage =='Asset group with provided name : ' + str(assetgroup.name) + "  already exists in this category"

    def test_create_asset_group_raise_exception(self,client,user,category):
        other_user = User.objects.create_user(username='other_user', password='password')
        self.user_login(client,other_user)
        other_user.email = user.email
        other_user.save()

        data = asset_group_test_data.get_default_asset_group_data()
        response = post_response_using_params(client,"create_asset_group",data,[category.id])
        assert_response_success(response,"404")


    def test_create_asset_group(self,client,user,category):
        self.initialize_user(user,False,False,True)
        data = asset_group_test_data.get_default_asset_group_data()
        self.user_login(client,user)
        response = post_response_using_params(client,"create_asset_group",data,[category.id])

        assert_response_redirect(response,"view_category")
        some = data['name']
        ag = AssetGroup.objects.get(name=data['name'])
        asset_group_test_data.assert_asset_group(ag,data,category)
################################################################################################################################
# Category
################################################################################################################################

@pytest.mark.django_db
class Test_Category_Views(BaseTest):
    
    def test_view_category_http404(self,client):
        other_user = User.objects.create_user(username='other_user', password='password')
        self.user_login(client, other_user)
        response = get_response_using_view_name(client,"view_networth")
        
        validate_response(response,200,b'InvestODiary -  404 Page','home/page-404.html')

    def test_view_categories(self,user,client,networth):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        # # Create some test data
        cat_1 = Category.objects.create(name='Test Cat 1', weightage=10, networth=networth)
        cat_2 = Category.objects.create(name='Test Cat 2', weightage=20, networth=networth)
        
        response = get_response_using_view_name(client,"view_networth")
        
        # Check that the response contains the asset type names
        assert cat_1.name in str(response.content)
        assert cat_2.name in str(response.content)
        
        # Check that the response status code is 200
        assert response.status_code == 200
    
    def test_view_categories_fully_allocated(self,user,client,networth):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        # # Create some test data
        cat_1 = Category.objects.create(name='Test Cat 1', weightage=50, networth=networth)
        cat_2 = Category.objects.create(name='Test Cat 2', weightage=50, networth=networth)
        
        response = get_response_using_view_name(client,"view_networth")
        
        # Check that the response contains the asset type names
        assert cat_1.name in str(response.content)
        assert cat_2.name in str(response.content)
        
        # Check that the response status code is 200
        assert response.status_code == 200
        validate_response(response,200,b'InvestODiary -  Configuration - Networth','home/configuration/networth.html')
        assert b'create_category' not in response.content
        assert b'type="submit">Add</a>' not in response.content
    

    def test_create_category_invalid_raise_exception(self,user,client):
        other_user = User.objects.create_user(username='other_user', password='password')
        self.user_login(client,other_user)
        other_user.email = user.email
        other_user.save()

        data = {
            'name': '$&^%#@',
            'weightage': -10
        }
        response = post_response_using_view_name(client,"create_category",data,user)
        assert_response_success(response,"404")

    def test_create_category_invalid_bad_form_data(self,user,client,networth,category):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        data = {
            'name': '$&^%#@',
            'weightage': -10
        }
        response = post_response_using_view_name(client,"create_category",data,user)

        validate_response(response,200,b'Add a new Category','home/configuration/create_category.html')

        assert 'form' in response.context
        form_errors = response.context["form"].errors
        assert form_errors["weightage"][0] == "Weightage must be greater than zero."
        assert form_errors["name"][0] == "Category Name must contain only letters, numbers, underscores or hyphens."

        weightage_used = networth.get_total_weightage_used() 
        available_weightage = 100 - weightage_used 

        over_weightage = available_weightage + 1

        data = {
            'name': 'some category',
            'weightage': over_weightage
        }
        response = post_response_using_view_name(client,"create_category",data,user)

        validate_response(response,200,b'Add a new Category','home/configuration/create_category.html')

        error_messsage = response.context["error_message"]
        assert error_messsage =='Invalid weightage. Weightage should be equal to or less than ' + str(available_weightage ) 

        # try creating a category with name same as existing category name
        data = {
            'name': category.name,
            'weightage': 10
        }
        
        response = post_response_using_view_name(client,"create_category",data,user)
        
        validate_response(response,200,b'Add a new Category','home/configuration/create_category.html')

        error_messsage = response.context["error_message"]
        assert error_messsage ==f'Category with same name already exist for this networth'

    def test_create_category(self,client,user,networth):
        self.initialize_user(user,False,False,True)
        data = category_test_data.get_default_category_data()
        self.user_login(client,user)
        response = post_response_using_view_name(client,"create_category",data,user)

        assert_response_redirect(response,"view_networth")

        category = Category.objects.get(name='Test Category')
        category_test_data.assert_category(category,data,networth)
    
    def test_edit_category_view_invalid_data(self, user,client,networth, category):
        
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)
       
        # Make a GET request to the edit category page
        response = client.get(reverse("edit_category", args=[category.id]))

        # Check that the response status code is 200
        assert response.status_code == 200

        # Make a POST request to update the category
        updated_name = "@$%"
        updated_weightage = -1
        data = category_test_data.set_default_category_data(updated_name,updated_weightage)

        response = post_response_using_params(client,"edit_category",data,[category.id])
        validate_response(response,200,b'InvestODiary -  Configuration - Networth','home/configuration/networth.html')
        assert 'form' in response.context
        form_errors = response.context["form"].errors
        assert form_errors["weightage"][0] == "Weightage must be greater than zero."
        assert form_errors["name"][0] == "Category Name must contain only letters, numbers, underscores or hyphens."

        weightage_used = networth.get_total_weightage_used() 

        previous_cat_weightage = category.weightage 
        available_weightage = 100 - weightage_used + previous_cat_weightage 
        over_weightage = available_weightage+1
        #updated_weightage_sum = weightage_used + category.weightage - previous_cat_weightage 

        # Make a POST request to update the category
        updated_name = "updated category new"
        updated_weightage = over_weightage
        data = category_test_data.set_default_category_data(updated_name,updated_weightage)

        response = post_response_using_params(client,"edit_category",data,[category.id])

        validate_response(response,200,b'InvestODiary -  Configuration - Networth','home/configuration/networth.html')
        error_messsage = response.context["error_message"]
        assert error_messsage =='Invalid weightage. Weightage should be equal to or less than ' + str(available_weightage ) 
        
    
    def test_edit_category_view(self, user,client,networth, category):
         
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)
       
        # Make a GET request to the edit category page
        response = client.get(reverse("edit_category", args=[category.id]))

        # Check that the response status code is 200
        assert response.status_code == 200

        # Make a POST request to update the category
        updated_name = "New Category Name"
        updated_weightage = 50

        data = set_default_asset_type_data(updated_name,updated_weightage)
        response = post_response_using_params(client,"edit_category",data,[category.id])

        # Check that the response status code is a redirect (302)
        assert response.status_code == 302

        # Check that the asset type was updated
        category.refresh_from_db()
        category_test_data.assert_category(category,data,networth)

    def test_delete_category(self,user,client,category):

        # create a user and log in
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)

        # send a delete request to the view with the asset type id
        response = delete_response_using_params(client,'delete_category',[category.id])

        # check that the response status code is 302 (redirect)
        assert response.status_code == 302

        # check that the asset type is deleted
        assert not Category.objects.filter(id=category.id).exists()

    def test_delete_category_invalid_user(self,client,category):

        other_user = User.objects.create_user(username='other_user', password='password')
        self.user_login(client, other_user)

        # send a delete request to the view with the asset type id
        response = delete_response_using_params(client,'delete_category',[category.id])
        
        assert_response_success(response,"404")

################################################################################################################################
# AssetType
################################################################################################################################

@pytest.mark.django_db
class Test_AssetType_Views(BaseTest):
    
    def test_view_asset_types_http404(self,client):
        other_user = User.objects.create_user(username='other_user', password='password')
        self.user_login(client, other_user)
        response = get_response_using_view_name(client,"view_asset_types")
        
        validate_response(response,200,b'InvestODiary -  404 Page','home/page-404.html')

    def test_view_asset_types(self,user,client,networth):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        # # Create some test data
        asset_type_1 = AssetType.objects.create(name='Test Asset Type 1', weightage=10, networth=networth)
        asset_type_2 = AssetType.objects.create(name='Test Asset Type 2', weightage=20, networth=networth)
        
        response = get_response_using_view_name(client,"view_asset_types")
        
        # Check that the response contains the asset type names
        assert asset_type_1.name in str(response.content)
        assert asset_type_2.name in str(response.content)
        
        # Check that the response status code is 200
        assert response.status_code == 200

    def test_create_asset_type_invalid_no_networth(self,client,user,networth):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        data = get_default_asset_type_data()
        networth_obj = Networth.objects.get(id=networth.id)
        networth_obj.delete()
        
        response = post_response_using_view_name(client,"create_asset_type",data,user)
        validate_response(response,200,b'Add a new Asset Type here','home/configuration/create_asset_type.html')
        assert 'error_message' in response.context
        assert response.context['error_message'] == 'Invalid data. Unable to create the asset type with provided input'

    def test_create_asset_type_invalid_bad_form_data(self,user,client,asset_type,networth):
        asset_type.networth = networth
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        data = {
            'name': '$&^%#@',
            'weightage': -10
        }
        response = post_response_using_view_name(client,"create_asset_type",data,user)

        validate_response(response,200,b'Add a new Asset Type here','home/configuration/create_asset_type.html')
        
        assert 'form' in response.context
        form_errors = response.context["form"].errors
        assert form_errors["weightage"][0] == "Weightage must be greater than zero."
        assert form_errors["name"][0] == "Asset-Type Name must contain only letters, numbers, underscores or hyphens."

    def test_create_asset_type(self,client,user,networth):
        self.initialize_user(user,False,False,True)
        data = get_default_asset_type_data()
        self.user_login(client,user)
        response = post_response_using_view_name(client,"create_asset_type",data,user)

        assert_response_redirect(response,"view_asset_types")

        asset_type = AssetType.objects.get(name='Test Asset Type')
        assert_asset_type(asset_type,data,networth)
    
    def test_edit_base_assettype_view_invalid_data(self, user,client,networth, asset_type):
        # Create an asset type
        asset_type.networth = networth
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)
       
        # Make a GET request to the edit asset type page
        response = client.get(reverse("edit_asset_type", args=[asset_type.id]))

        # Check that the response status code is 200
        assert response.status_code == 200

        # Make a POST request to update the asset type
        updated_name = "@$%"
        updated_weightage = -1
        data = set_default_asset_type_data(updated_name,updated_weightage)

        response = post_response_using_params(client,"edit_asset_type",data,[asset_type.id])
        validate_response(response,200,b'InvestODiary -  Configuration - Asset Type','home/configuration/asset_types.html')
        assert 'form' in response.context
        form_errors = response.context["form"].errors
        assert form_errors["weightage"][0] == "Weightage must be greater than zero."
        assert form_errors["name"][0] == "Asset-Type Name must contain only letters, numbers, underscores or hyphens."

    def test_edit_asset_type_view(self, user,client,networth, asset_type):
         # Create an asset type
        asset_type.networth = networth
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)
       
        # Make a GET request to the edit asset type page
        response = client.get(reverse("edit_asset_type", args=[asset_type.id]))

        # Check that the response status code is 200
        assert response.status_code == 200

        # Make a POST request to update the asset type
        updated_name = "New Asset Type Name"
        updated_weightage = 50

        data = set_default_asset_type_data(updated_name,updated_weightage)
        response = post_response_using_params(client,"edit_asset_type",data,[asset_type.id])

        # Check that the response status code is a redirect (302)
        assert response.status_code == 302

        # Check that the asset type was updated
        asset_type.refresh_from_db()
        assert_asset_type(asset_type,data,networth)


    def test_delete_asset_type(self,user,client,asset_type):

        # create a user and log in
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)

        # send a delete request to the view with the asset type id
        response = delete_response_using_params(client,'delete_asset_type',[asset_type.id])

        # check that the response status code is 302 (redirect)
        assert response.status_code == 302

        # check that the asset type is deleted
        assert not AssetType.objects.filter(id=asset_type.id).exists()

################################################################################################################################
# BaseUnit
################################################################################################################################

@pytest.mark.django_db
class Test_BaseUnit_Views(BaseTest):

    def test_view_base_units_raise_exception(self,user,client,networth):
        other_user = User.objects.create_user(username='other_user', password='password')
        self.user_login(client,other_user)
        other_user.email = user.email
        other_user.save()

        base_unit_1 = BaseUnit.objects.get(networth=networth)
        base_unit_1.networth = networth
        base_unit_1.save()
        response = get_response_using_view_name(client,"view_base_unit")
        assert_response_success(response,"404")
   
    def test_view_base_units_single(self,user,client,networth):
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)
        
        # # Create only single test data
        base_unit_1 = BaseUnit.objects.get(networth=networth)
        
        response = get_response_using_view_name(client,"view_base_unit")
        
        assert_response_success(response,"view_base_unit")
        # Check that the response contains the asset type names
        assert base_unit_1.name in str(response.content)
    
    def test_create_base_unit_invalid_no_networth(self,client,user,networth):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        data = get_default_base_unit_data()
        networth_obj = Networth.objects.get(id=networth.id)
        networth_obj.delete()
        
        response = post_response_using_view_name(client,"create_base_unit",data=data,user=user)

        validate_response(response,200,b'Add a new Base Unit here','home/configuration/create_base_unit.html')
        assert 'error_message' in response.context
        assert response.context['error_message'] == 'Invalid form. Please correct the errors below.'

    def test_create_base_unit_view_GET(self,client,user):
            #Initialize user with customer role
            self.initialize_user(user,False,False,True)
            self.user_login(client, user)
            # Make a GET request to the create base unit page
            response = get_response_using_view_name(client,"create_base_unit")

            validate_response(response,200,b'name="csrfmiddlewaretoken"','home/configuration/create_base_unit.html')
            assert b'<input' in response.content

    def test_create_base_unit_view(self,user,client,networth):
            self.initialize_user(user,False,False,True)
            self.user_login(client, user)
            data = get_default_base_unit_data()

            response = post_response_using_view_name(client,"create_base_unit",data,user)

            assert_response_redirect(response,'view_base_unit')

            base_unit = BaseUnit.objects.get(networth=networth)
            assert_base_unit_default(base_unit,networth)
    
    def test_edit_base_unit_view_raise_exception_get(self, user,client,networth):
         # Create a base unit
        other_user = User.objects.create_user(username='other_user', password='password')
        self.user_login(client,other_user)
        other_user.email = user.email
        other_user.save()

        base_unit_1 = BaseUnit.objects.get(networth=networth)
        base_unit_1.networth = networth
        base_unit_1.save()
       
        # Make a GET request to the edit base unit page
        response = client.get(reverse("edit_base_unit", args=[base_unit_1.id]))

        # Check that the response status code is 200
        assert_response_success(response,"404")

    def test_edit_base_unit_view_invalid_data(self, user,client,networth, base_unit):
         # Create a base unit
        base_unit.networth = networth
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)
       
        # Make a GET request to the edit base unit page
        response = client.get(reverse("edit_base_unit", args=[base_unit.id]))

        # Check that the response status code is 200
        assert response.status_code == 200

        # Make a POST request to update the base unit
        updated_name = '#@!$'
        updated_value = -1
        data = set_default_base_unit_data(updated_name,updated_value)
        response = post_response_using_params(client,"edit_base_unit",data,param_set=[base_unit.id])
        
        validate_response(response,200,b'InvestODiary -  Base Unit Configuration','home/configuration/base_unit.html')

        assert 'form' in response.context
        form_errors = response.context["form"].errors
        assert form_errors["value"][0] == "Value must be greater than zero."
        assert form_errors["name"][0] == "Base Unit Name must contain only letters, numbers, underscores or hyphens."
    
    def test_edit_base_unit_view(self, user,client,networth, base_unit):
         # Create a base unit
        base_unit.networth = networth
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)
       
        # Make a GET request to the edit base unit page
        response = client.get(reverse("edit_base_unit", args=[base_unit.id]))

        # Check that the response status code is 200
        assert response.status_code == 200

        # Make a POST request to update the base unit
        updated_name = "New BaseUnit Name"
        updated_value = 50
        data = set_default_base_unit_data(updated_name,updated_value)

        response = post_response_using_params(client,'edit_base_unit',data,param_set=[base_unit.id])

        # Check that the response status code is a redirect (302)
        assert response.status_code == 302

        # Check that the asset type was updated
        base_unit.refresh_from_db()
        assert_base_unit(base_unit,data,networth)
    
    # def test_delete_base_unit(self,user,client,base_unit):

    #     # create a user and log in
    #     self.initialize_user(user,False,False,True)
    #     self.user_login(client, user)

    #     # send a delete request to the view with the base unit id
    #     response = delete_response_using_params(client,'delete_base_unit',param_set=[base_unit.id])
        
    #     # check that the response status code is 302 (redirect)
    #     assert response.status_code == 302

    #     # check that the base unit is deleted
    #     assert not AssetType.objects.filter(id=base_unit.id).exists()
################################################################################################################################
# Networth
################################################################################################################################

@pytest.mark.django_db
class TestNetworthViews(BaseTest):

    def test_edit_networth_view(self, user,client,networth, base_unit):
        # Create a base unit
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)

        # Make a GET request to the edit base unit page
        response = client.get(reverse("edit_networth", args=[networth.id]))

        # Check that the response status code is 200
        assert response.status_code == 200

        # Make a POST request to update the base unit
        updated_name = "New networth Name"
        updated_value = 50
        data = networth_test_data.set_default_networth_data(updated_name,updated_value,True)

        response = post_response_using_params(client,'edit_networth',data,param_set=[networth.id])

        # Check that the response status code is a redirect (302)
        assert response.status_code == 302

        # Check that the asset type was updated
        networth.refresh_from_db()
        networth_test_data.assert_networth(networth,data,user)

    def test_edit_networth_view_invalid_data(self, user,client,networth, base_unit):
         # Create a base unit
        base_unit.networth = networth
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)
       
        # Make a GET request to the edit networth page
        response = client.get(reverse("edit_networth", args=[networth.id]))

        # Check that the response status code is 200
        assert response.status_code == 200

        # Make a POST request to update the networth
        updated_name = '#@!$'
        updated_value = -1
        updated_is_active = False
        data = networth_test_data.set_default_networth_data(updated_name,updated_value,updated_is_active)
        response = post_response_using_params(client,"edit_networth",data,param_set=[networth.id])
        
        validate_response(response,200,b'Configuration - Networth','home/configuration/networth_settings.html')

        assert 'form' in response.context
        form_errors = response.context["form"].errors
        assert form_errors["amount"][0] == "Amount must be greater than zero."
        assert form_errors["name"][0] == "Networth Name must contain only letters, numbers, underscores or hyphens."    
    

