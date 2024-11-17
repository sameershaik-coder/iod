import pytest
from tests.test_classes import BaseTest
from django.urls import reverse
from test_common import (
    delete_response_using_params,
    get_response_using_view_name,
    assert_response_success,
    assert_data_in_context,
    post_response_using_params
)
from tests.common.test_data.user_profile import (
    set_default_userprofile_data
)
from tests.common.test_data import nominee as nominee_testdata
from test_common import (
    get_response_using_view_name,
    post_response_using_view_name,
    validate_response,
    assert_response_redirect,
    assert_response_success
)
from apps.home.models import(
    UserNominee,
    UserProfile
)
from django.contrib.auth.models import User
from apps.home.actions import nominee as nominee_actions
@pytest.mark.django_db
class Test_Nominee_Views(BaseTest):
    def test_nominee_edit_raise_exception(self,client,user,nominee,mocker):
        mocker.patch.object(nominee_actions, 'update_model_fields', side_effect=Exception("Simulated error"))
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)

        data = nominee_testdata.get_default_nominee_data()
        response = post_response_using_params(client,"edit_nominee",data,[nominee.id])
        assert_response_success(response, "500")

    def test_nominee_create_raise_exception(self,client,user,mocker):
        # Mocking the 'do_create_nominee' function to raise an exception when called
        mocker.patch.object(nominee_actions, 'do_create_nominee', side_effect=Exception("Simulated error"))

        self.initialize_user(user,False,False,True)
        self.user_login(client,user)

        # Prepare test data for nominee creation
        data = nominee_testdata.get_default_nominee_data()

        # Make a POST request using the view name 'create_nominee' and the test data
        response = post_response_using_view_name(client, "create_nominee", data, user)

        # Assert that the response is an error (status code 500)
        assert_response_success(response, "500")

    def test_nominee_view_raise_exception(self,client,user):
        other_user = User.objects.create_user(username='other_user', password='password')
        self.user_login(client,other_user)
        other_user.email = user.email
        other_user.save()
        url = reverse('view_nominee')
        response = client.post(url)
        assert_response_success(response,"500")

    def test_nominee_view_authenticated_user_GET(self,client,user):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        response = get_response_using_view_name(client,"create_nominee")
        assert_response_success(response,'create_nominee')
        assert_data_in_context(response,['form'])

    def test_nominee_view_unauthenticated_user_GET(self,client,user):
        url = reverse('create_nominee')
        response = client.get(url)
        response = get_response_using_view_name(client,"create_nominee")
        assert response.status_code == 302
        assert response.url == '/login/?next=' + url
    
    def test_nominee_create_POST(self,client,user):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        # Make a POST request to create the nominee
        data = nominee_testdata.get_default_nominee_data()
        
        response = post_response_using_view_name(client,"create_nominee",data,user)
        
        assert_response_redirect(response,'view_nominee')
        nominee1 = UserNominee.objects.get(email=data["email"])
        nominee_testdata.assert_nominee(nominee1,data,user)
    
    def test_nominee_create_invalid_data(self,client,user):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        data ={
            'name' : '$&^%#@',
            'email' : '$&^%#@.com',
            'status' : 'A'
        }
        response = post_response_using_view_name(client,"create_nominee",data,user)
        validate_response(response,200,b'Add a new Nominee','home/create_nominee.html')
        assert 'form' in response.context
        form_errors = response.context["form"].errors
        assert form_errors["name"][0] == "Nominee Name must contain only letters"
        assert form_errors["email"][0] == "Please enter a valid email address."

    def test_nominee_edit_POST(self,client,user,nominee):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        response = client.get(reverse("edit_nominee", kwargs={'pk': nominee.id}))
        # Check that the response status code is 200
        assert response.status_code == 200

        updated_name = "updated nom name"
        updated_email = "updated@testmail.com"

        data = nominee_testdata.set_default_nominee_data(updated_name,updated_email,"A")
        response = post_response_using_params(client,"edit_nominee",data,[nominee.id])

        # Check that the response status code is a redirect (302)
        assert response.status_code == 302

        nominee.refresh_from_db()
        nominee_testdata.assert_nominee(nominee,data,user)

    def test_nominee_edit_user_GET(self,client,user,nominee):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        response = client.get(reverse("edit_nominee", kwargs={'pk': nominee.id}))
        assert_response_success(response,'edit_nominee')
        assert_data_in_context(response,['form'])
    
    def test_nominee_edit_POST_invalid_data(self,client,user,nominee):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        response = client.get(reverse("edit_nominee", kwargs={'pk': nominee.id}))
        # Check that the response status code is 200
        assert response.status_code == 200

        updated_name = "####$@!$%$$"
        updated_email = "$@@$@()*@testmail.com"

        data = nominee_testdata.set_default_nominee_data(updated_name,updated_email,"A")
        response = post_response_using_params(client,"edit_nominee",data,[nominee.id])

        validate_response(response,200,b'InvestODiary -  Edit Nominee','home/edit_nominee.html')
        assert 'form' in response.context
        form_errors = response.context["form"].errors
        assert form_errors["name"][0] == "Nominee Name must contain only letters"
        assert form_errors["email"][0] == "Please enter a valid email address."
    
    def test_viewnominee_user_GET(self,client,user,nominee):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        url = reverse('view_nominee')
        response = client.get(url)

        assert nominee.name in str(response.content)
        assert nominee.email in str(response.content)
        assert nominee.status in str(response.content)
        assert "No Nominee has been set yet." not in str(response.content)
        assert response.status_code == 200
    
    def test_viewnominee_user_GET_no_nominee(self,client,user):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        url = reverse('view_nominee')
        response = client.get(url)

        assert "No Nominee has been set yet." in str(response.content)
        assert "Add" in str(response.content)
        assert response.status_code == 200

    def test_delete_nominee(self,client,user,nominee):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        # send a delete request to the view with the asset type id
        response = delete_response_using_params(client,'delete_nominee',[nominee.id])
        # check that the response status code is 302 (redirect)
        assert response.status_code == 302

        # check that the asset type is deleted
        assert not UserNominee.objects.filter(id=nominee.id).exists() 
    
    def test_delete_nominee_invalid_user(self,client,user,nominee):
        other_user = User.objects.create_user(username='other_user', password='password')
        self.user_login(client, other_user)
        # send a delete request to the view with the asset type id
        response = delete_response_using_params(client,'delete_nominee',[nominee.id])
        # check that the response status code is 302 (redirect)
        assert response.status_code == 200

        # check that the asset type is deleted
        assert UserNominee.objects.filter(id=nominee.id).exists() == True
        assert_response_success(response,"500")


