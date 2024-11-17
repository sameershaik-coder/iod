import pytest
from tests.test_classes import BaseTest
from django.urls import reverse
from django.contrib.auth.models import User
from test_common import (
    get_response_using_view_name,
    assert_response_success,
    assert_response_redirect
)

@pytest.mark.django_db
class Test_Home_Views(BaseTest):
    def test_home_view_authenticated_user(self,user,client,networth,base_unit,assetgroup,instrument):
        """
        Test assets view for an authenticated user
        """
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        # Create a request
        response = get_response_using_view_name(client,"home")

        assert response.status_code == 302
    

################################################################################################################################
# Other pages
################################################################################################################################
    def test_home_pages_view(self,user,client,networth,base_unit,assetgroup,instrument):
        """
        pages admin
        """
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        # Create a request
        url = "/app/someurl"
        response = client.get(url)
        assert_response_success(response,"404")

        url = "/admin/"
        response = client.get(url)
        assert response.status_code == 302
        assert "/admin/" in str(response.url)

    def test_home_pages_view_admin_logged_in(self,user,client,networth,base_unit,assetgroup,instrument):
        """
        pages admin
        """
        self.initialize_user(user,True,True,True)
        user_obj = User.objects.get(id=user.id)
        user_obj.is_active = True
        user_obj.is_superuser = True
        user_obj.save()
        self.user_login(client,user)
        url = "/admin/"
        response = client.get(url)
        assert response.status_code == 200
        assert '<td><a href="/admin/auth/group/" class="changelink" aria-describedby="auth-group">Change</a></td>' in str(response.content)

    
    def test_home_pages_view_non_admin_logged_in(self,user,client,networth,base_unit,assetgroup,instrument):
        """
        pages admin
        """
        self.initialize_user(user,False,False,True)
        user_obj = User.objects.get(id=user.id)
        user_obj.is_active = True
        user_obj.is_superuser = False
        user_obj.save()
        self.user_login(client,user)

        url = "/admin/"
        response = client.get(url)
        assert_response_redirect(response,"login")
    
        
