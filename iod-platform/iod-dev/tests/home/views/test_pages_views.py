import pytest
from django.urls import reverse
from django.http import HttpResponse
from django.template import TemplateDoesNotExist
from django.test import Client
from unittest.mock import patch
from django.contrib.auth.models import User
from tests.test_classes import BaseTest
@pytest.mark.django_db
class TestPagesView(BaseTest):
    
    @pytest.fixture
    def authenticated_client(self, client):
        # Create and log in a test user
        user = User.objects.create_user(username='testuser', password='testpass')
        client.login(username='testuser', password='testpass')
        return client

    def test_valid_template(self, client,user):
        # Test for a valid template
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        response = client.get('/app/homesasaspage.html')
        #response = authenticated_client.get('/home/somepage.html')
        assert response.status_code == 200
        assert 'home/page-404.html' in [t.name for t in response.templates]
    
    def test_redirect_to_admin(self, client, user):
        # Test if accessing 'admin' redirects to the admin index
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        response = client.get('/app/admin')
        assert response.status_code == 302  # Should be a redirect
        assert response.url == reverse('admin:index')
