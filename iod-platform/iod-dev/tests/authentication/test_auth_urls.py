from django.urls import reverse
import pytest
from tests.test_classes import BaseTest
from django.contrib.auth.views import PasswordChangeDoneView

@pytest.mark.django_db
class Test_Authentication_Urls(BaseTest):

    def test_view_auth_login(self,client):
        response = client.get(reverse("login"))

        assert response.status_code == 200

    def test_view_auth_logout(self,client,user):
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)
        response = client.get(reverse("logout"))

        assert response.status_code == 302

    def test_view_auth_register(self,client):
        response = client.get(reverse("register"))

        assert response.status_code == 200

    def test_change_password_url_resolves(self,client,user):
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)
        url = reverse('change_password')
        print(url)
        assert url == '/app/auth/change-password/'
        response = client.get(url)
        assert response.status_code == 200
    
    def test_change_password_view_accessible_by_name(self,client,user):
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)
        response = client.get(reverse('change_password'))
        assert response.status_code == 200
    
    def test_change_password_done_view(self,client,user):
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)
        url = reverse('password_change_done')
        response = client.get(url)

        # Check that the response status code is 200 (OK)
        assert response.status_code == 200

         # Check that the correct template is being used
        assert 'accounts/change-password/password_change_done.html' in [t.name for t in response.templates]

        # Check that the view is an instance of PasswordChangeDoneView
        assert isinstance(response.context['view'], PasswordChangeDoneView)

    