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
from apps.authentication.views import CustomPasswordChangeForm
from django.core import mail
import re

@pytest.mark.django_db
class Test_Auth_ForgotPassword_View(BaseTest):
    
    def test_custom_password_reset_view(self,client, user):
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)
        # Get the url for the custom password reset view
        url = reverse("custom_password_reset")
        # Get the response from the client by sending a GET request to the url
        response = client.get(url)
        # Assert that the response status code is 200 (OK)
        assert response.status_code == 200
        # Assert that the response contains the expected template
        assert "accounts/registration/password_reset_form.html" in response.template_name
        # Get the response from the client by sending a POST request to the url with the test user's email
        response = client.post(url, {"email": user.email})
        # Assert that the response status code is 302 (Found)
        assert response.status_code == 302
        # Assert that the response redirects to the password reset done view
        assert response.url == reverse("password_reset_done")
        # Assert that an email was sent to the test user
        assert len(mail.outbox) == 1
        # Get the email subject and body
        subject = mail.outbox[0].subject
        body = mail.outbox[0].body
        # Assert that the email subject contains the expected text
        assert "Password reset" in subject
        # Assert that the email body contains the test user's username and email
        assert user.username in body
        assert user.email in body
        # Assert that the email body contains a link to the password reset confirm view
        assert "You're receiving this email because you requested a password reset for your user account at" in body

    
    # Define a test function to test the password reset confirm view
    def test_password_reset_confirm_view2(self,client, user):
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)
        # Get the url for the custom password reset view
        url = reverse("custom_password_reset")
        # Get the response from the client by sending a GET request to the url
        response = client.get(url)
        # Assert that the response status code is 200 (OK)
        assert response.status_code == 200
        # Assert that the response contains the expected template
        assert "accounts/registration/password_reset_form.html" in response.template_name
        # Get the response from the client by sending a POST request to the url with the test user's email
        response = client.post(url, {"email": user.email})
        # Assert that the response status code is 302 (Found)
        assert response.status_code == 302
        # Assert that the response redirects to the password reset done view
        assert response.url == reverse("password_reset_done")
        # Assert that an email was sent to the test user
        assert len(mail.outbox) == 1
        # Get the email subject and body
        subject = mail.outbox[0].subject
        body = mail.outbox[0].body
        # Define a regular expression pattern to match the url that starts with http
        pattern = r"http://\S+"

        # Use the re.search function to find the first match of the pattern in the text
        match = re.search(pattern, body)

        # If a match is found, print the matched url
        if match:
            url = match.group()
            print(f"The url that starts with http is: {url}")
            reset_url_link = url
            # Get the response from the client by sending a POST request to the url with the new password
            new_password = "Test@123"
            response = client.post(reset_url_link)
            #print(response.content.decode())
            # Assert that the response status code is 302 (Found)
            assert response.status_code == 302
            final_url = response.url
            response = client.post(final_url,{"new_password1": new_password, "new_password2": new_password})
            
            # Assert that the response redirects to the password reset complete view
            assert response.url == reverse("password_reset_complete")
            # Get the updated test user from the database
            user = User.objects.get(id=user.id)
            # Assert that the test user's password was changed to the new password
            assert user.check_password(new_password)  
        # Otherwise, print a message that no url was found
        else:
            # Fail the testcase
            assert 1 == 2
 
    # Define a test function to test the password reset complete view
    def test_password_reset_complete_view(SELF, client, user):
        # Get the url for the password reset complete view
        url = reverse("password_reset_complete")
        # Get the response from the client by sending a GET request to the url
        response = client.get(url)
        # Assert that the response status code is 200 (OK)
        assert response.status_code == 200
        # Assert that the response contains the expected template
        assert "accounts/registration/password_reset_complete.html" in response.template_name
        some = response.content.decode()  
        # Assert that the response contains the expected message
        assert "Password reset complete" in response.content.decode()  


@pytest.mark.django_db
class Test_Auth_ChangePassword_View(BaseTest):
    
    def test_change_password_view_get(self,client, user):
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)
        response = client.get(reverse('change_password'))

        assert response.status_code == 200
        assert 'accounts/change-password/change_password.html' in [t.name for t in response.templates]
        assert isinstance(response.context['form'], CustomPasswordChangeForm)

    def test_change_password_view_post_valid(self,client, user):
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)
        new_password = 'newpassword@123'
        response = client.post(reverse('change_password'), {'old_password': "Test@123", 'new_password1': new_password, 'new_password2': new_password})

        assert response.status_code == 302  # Redirect to password_change_done view

        # Ensure the password is actually changed
        user.refresh_from_db()
        assert user.check_password(new_password)

    def test_change_password_view_post_invalid_oldpassword(self,client, user):
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)
        response = client.post(reverse('change_password'), {'old_password': 'wrongpassword', 'new_password1': 'newpassword', 'new_password2': 'newpassword'})

        # incorrect old password

        assert response.status_code == 200  # Stay on the same page for invalid form submission
        assert 'accounts/change-password/change_password.html' in [t.name for t in response.templates]
        assert isinstance(response.context['form'], CustomPasswordChangeForm)
        assert 'form' in response.context
        assert response.context['form'].errors['old_password'][0] == 'Your old password was entered incorrectly. Please enter it again.'

        # check with old password as empty
        response = client.post(reverse('change_password'), {'old_password': '', 'new_password1': 'newpassword', 'new_password2': 'newpassword'})

        assert response.status_code == 200  # Stay on the same page for invalid form submission
        assert 'accounts/change-password/change_password.html' in [t.name for t in response.templates]
        assert isinstance(response.context['form'], CustomPasswordChangeForm)
        assert 'form' in response.context
        assert response.context['form'].errors['old_password'][0] == 'This field is required.'

    def test_change_password_view_post_invalid_newpassword(self,client, user):
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)
        response = client.post(reverse('change_password'), {'old_password': 'Test@123', 'new_password1': '', 'new_password2': ''})

        assert response.status_code == 200  # Stay on the same page for invalid form submission
        assert 'accounts/change-password/change_password.html' in [t.name for t in response.templates]
        assert isinstance(response.context['form'], CustomPasswordChangeForm)
        assert 'form' in response.context
        assert response.context['form'].errors['new_password1'][0] == 'This field is required.'
        assert response.context['form'].errors['new_password2'][0] == 'This field is required.'

        #only new password 1 empty
        response = client.post(reverse('change_password'), {'old_password': 'Test@123', 'new_password1': '', 'new_password2': 'some@123333'})

        assert response.status_code == 200  # Stay on the same page for invalid form submission
        assert 'accounts/change-password/change_password.html' in [t.name for t in response.templates]
        assert isinstance(response.context['form'], CustomPasswordChangeForm)
        assert 'form' in response.context
        assert response.context['form'].errors['new_password1'][0] == 'This field is required.'

        #only new password 2 empty
        response = client.post(reverse('change_password'), {'old_password': 'Test@123', 'new_password1': 'some@123333', 'new_password2': ''})

        assert response.status_code == 200  # Stay on the same page for invalid form submission
        assert 'accounts/change-password/change_password.html' in [t.name for t in response.templates]
        assert isinstance(response.context['form'], CustomPasswordChangeForm)
        assert 'form' in response.context
        assert response.context['form'].errors['new_password2'][0] == 'This field is required.'
        
        #only new password only digits
        response = client.post(reverse('change_password'), {'old_password': 'Test@123', 'new_password1': '1233123333', 'new_password2': '1233123333'})

        assert response.status_code == 200  # Stay on the same page for invalid form submission
        assert 'accounts/change-password/change_password.html' in [t.name for t in response.templates]
        assert isinstance(response.context['form'], CustomPasswordChangeForm)
        assert 'form' in response.context
        assert response.context['form'].errors['new_password2'][0] == 'This password is entirely numeric.'

        #only new password only letters 4
        response = client.post(reverse('change_password'), {'old_password': 'Test@123', 'new_password1': 'sajk', 'new_password2': 'sajk'})

        assert response.status_code == 200  # Stay on the same page for invalid form submission
        assert 'accounts/change-password/change_password.html' in [t.name for t in response.templates]
        assert isinstance(response.context['form'], CustomPasswordChangeForm)
        assert 'form' in response.context
        assert response.context['form'].errors['new_password2'][0] == 'This password is too short. It must contain at least 8 characters.'

    


@pytest.mark.django_db
class Test_Auth_Login_View(BaseTest):
    def test_login_view_valid(self,client,user):
        user_obj = User.objects.create_user(
            username='testuser@mail.com',password='testpass', email='testuser@mail.com'
        )
        url = reverse('login')
        response = client.get(url)
        assert response.status_code == 200

        # Test valid login
        data = {'email': 'testuser@mail.com', 'password': 'testpass'}
        response = client.post(url, data)
        assert response.status_code == 302
        assert response.url == '/app/'
        assert response.wsgi_request.user.is_authenticated == True

    def test_login_view_invalid(self,client,user):
        # Test invalid login
        data = {'email': 'testuser@mail.com', 'password': 'wrongpass'}
        url = reverse('login')
        response = client.post(url, data)
        assert response.status_code == 200
        assert not response.wsgi_request.user.is_authenticated 

    def test_login_view_invalid_form(self,client):
        response = client.post(reverse('login'), {'email': '!!!@-', 'password': ''})
        assert response.status_code == 200
        assert b'Error validating the form' in response.content
        assert not response.wsgi_request.user.is_authenticated

class Test_Auth_Register_View(BaseTest):
    def test_register_user_view_get(self,client):
        response = client.get(reverse('register'))
        assert response.status_code == 200
    
    def test_register_user_view_get_template(self,client):
        response = client.get(reverse('register'))
        assert response.status_code == 200
        assert 'accounts/register.html' in [t.name for t in response.templates]

    def test_register_user_view_post_success(self,client, django_user_model):
        email = 'test@example.com'
        password = 'testpass123'
        country = "IN"
        data = {
            'email': email,
            'password1': password,
            'password2': password,
            'country': country
        }
        response = client.post(reverse('register'), data=data)
        assert response.status_code == 200
        assert django_user_model.objects.filter(username=email).exists()
        assert response.context['success']
        assert response.context['msg'] == 'User registration successful. Please click Sign In.'
        

    def test_register_user_view_post_invalid(self,client):
        country = "ABC"
        data = {
            'email': 'invalidemail',
            'password1': 'testpass123',
            'password2': 'testpass456',
            'country': country
        }
        response = client.post(reverse('register'), data=data)
        assert response.status_code == 200
        assert 'Provided data is not valid' in response.context['msg']
        assert not response.context['success']
    
    def test_register_user_view_post_invalid_existing_email(self,client,user):
        password = 'testpass123'
        country = "IN"
        data = {
            'email': 'test@example.com',
            'password1': password,
            'password2': password,
            'country': country
        }
        response = client.post(reverse('register'), data=data)
        password = 'testpass123'
        country = "IN"
        data = {
            'email': 'test@example.com',
            'password1': password,
            'password2': password,
            'country': country
        }
        response = client.post(reverse('register'), data=data)
        assert response.status_code == 200
        assert 'User with provided email already exists. Please choose another email' in response.context['msg']
        assert not response.context['success']

