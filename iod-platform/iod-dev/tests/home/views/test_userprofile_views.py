import pytest
from tests.test_classes import BaseTest
from django.urls import reverse
from test_common import (
    get_response_using_view_name,
    assert_response_success,
    assert_data_in_context
)
from tests.common.test_data.user_profile import (
    get_default_userprofile_data,
    set_default_userprofile_data
)
from test_common import (
    get_response_using_view_name,
    post_response_using_view_name,
    validate_response,
    assert_response_redirect,
    assert_response_success
)
from apps.home.models import(
    UserProfile,
)
from django.contrib.auth.models import User

@pytest.mark.django_db
class Test_UserProfile_Views(BaseTest):
    def test_userprofile_view_authenticated_user_GET(self,client,user):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        response = get_response_using_view_name(client,"view_profile")
        assert_response_success(response,'view_profile')
        assert_data_in_context(response,['form'])
    
    def test_networth_view_unauthenticated_user(self,client):
        url = reverse('view_profile')
        response = client.get(url)
        assert response.status_code == 302
        assert response.url == '/login/?next=' + url
    
    def test_userprofile_edit_POST(self,client,user):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        # Make a POST request to update the base unit
        updated_fname = 'updated first name'
        updated_lname = 'updated last name'
        updated_address = 'updated address'
        updated_bio = 'updated bio'
        data = set_default_userprofile_data(updated_fname,updated_lname,updated_address,updated_bio)
        response = post_response_using_view_name(client,"view_profile",data,user)
        
        assert_response_redirect(response,'view_profile')
    
    def test_userprofile_edit_invalid_raise_exception(self,client,user):
        other_user = User.objects.create_user(username='other_user', password='password')
        self.user_login(client,other_user)
        other_user.email = user.email
        other_user.save()
        data = get_default_userprofile_data()
        response = post_response_using_view_name(client,"view_profile",data,user)
        assert_response_success(response,"500")

    def test_userprofile_edit_invalid_data_POST(self,client,user):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        # Make a POST request to update the base unit
        updated_fname = '999'
        updated_lname = '#@$'
        updated_address = '||~!'
        updated_bio = '<div></div> SELECT'
        data = set_default_userprofile_data(updated_fname,updated_lname,updated_address,updated_bio)
        response = post_response_using_view_name(client,"view_profile",data,user)
        
        validate_response(response,200,b'InvestODiary -  Profile','home/edit_profile.html')
        
        assert 'form' in response.context
        form_errors = response.context["form"].errors
        assert form_errors["first_name"][0] == "Invalid first name. First name must contain only letters"
        assert form_errors["last_name"][0] == "Invalid last name. Last name must contain only letters"
        assert form_errors["address"][0] == "Invalid address. The address should only contain alphanumeric characters, whitespace, hyphens, dots, commas, and hash characters."
        assert form_errors["bio"][0] == "HTML or programming tags are not allowed."
        assert form_errors["bio"][1] == "SQL statements are not allowed."
    
    def test_user_create_default_userprofile(self,client,user):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        profile = UserProfile.objects.get(user=user)
        assert profile is not None
        assert profile.first_name is None
        assert profile.last_name is None
        assert profile.address is None
        assert profile.bio is None
    
    def test_userprofile_viewnominee_exists(self,client,user,nominee):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        profile = UserProfile.objects.get(user=user)
        url = reverse('view_profile')
        response = client.get(url)
        validate_response(response,200,b'InvestODiary -  Profile','home/edit_profile.html')
        validate_response(response,200,nominee.name.encode(),'home/edit_profile.html')
    
    def test_userprofile_viewnominee_not_exists(self,client,user):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        profile = UserProfile.objects.get(user=user)
        url = reverse('view_profile')
        response = client.get(url)
        validate_response(response,200,b'InvestODiary -  Profile','home/edit_profile.html')
        validate_response(response,200,b'None','home/edit_profile.html')
        
