import pytest
from tests.common.test_data.networth import assert_networth, set_default_networth_data
from tests.test_classes import BaseTest
from django.urls import reverse
from test_common import (
    get_response_using_view_name,
    assert_response_success,
    assert_data_in_context,
    post_response_using_params,
    validate_response
)
from django.contrib.auth.models import User

@pytest.mark.django_db
class Test_Networth_Views(BaseTest):
    
    def test_networth_settings_edit_raise_exception(self,client,user,networth):
        other_user = User.objects.create_user(username='other_user', password='password')
        self.user_login(client,other_user)
        other_user.email = user.email
        other_user.save()

        # Make a POST request to update the category
        updated_name = "New Networth Name"
        updated_amount = 50
        data = set_default_networth_data(updated_name,updated_amount,True)
        response = post_response_using_params(client,"edit_networth_settings",data,[networth.id])
        assert_response_success(response,"500")

    def test_networth_settings_view_raise_exception(self,client,user):
        other_user = User.objects.create_user(username='other_user', password='password')
        self.user_login(client,other_user)
        other_user.email = user.email
        other_user.save()

        response = get_response_using_view_name(client,"view_networth_settings")
        assert_response_success(response,"500")

    def test_networth_settings_view_authenticated_user(self,client,user,networth,base_unit,category,assetgroup,instrument):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        response = get_response_using_view_name(client,"view_networth_settings")
        assert_response_success(response,'settings')

    def test_networth_view_unauthenticated_user(self,client):
        url = reverse('view_networth_settings')
        response = client.get(url)
        assert response.status_code == 302
        assert response.url == '/login/?next=' + url

    
    def test_edit_networth_settings_view_invalid_data(self, user,client,networth):
        
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)
       
        # Make a GET request to the edit category page
        response = client.get(reverse("edit_networth_settings", args=[networth.id]))

        # Check that the response status code is 200
        assert response.status_code == 200

        # Make a POST request to update the category
        updated_name = "@$%"
        updated_amount = -1
        data = set_default_networth_data(updated_name,updated_amount,True)

        response = post_response_using_params(client,"edit_networth_settings",data,[networth.id])
        validate_response(response,200,b'InvestODiary -  Settings','home/networth_settings.html')
        assert 'form' in response.context
        form_errors = response.context["form"].errors
        assert form_errors["amount"][0] == "Amount must be greater than zero."
        assert form_errors["name"][0] == "Networth Name must contain only letters, numbers, underscores or hyphens."
    
    def test_edit_networth_settings_view(self, user,client,networth):
         
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)
       
        # Make a GET request to the edit category page
        response = client.get(reverse("edit_networth_settings", args=[networth.id]))

        # Check that the response status code is 200
        assert response.status_code == 200

        # Make a POST request to update the category
        updated_name = "New Networth Name"
        updated_amount = 50

        data = set_default_networth_data(updated_name,updated_amount,True)
        response = post_response_using_params(client,"edit_networth_settings",data,[networth.id])

        # Check that the response status code is a redirect (302)
        assert response.status_code == 302

        # Check that the asset type was updated
        networth.refresh_from_db()
        assert_networth(networth,data,user)