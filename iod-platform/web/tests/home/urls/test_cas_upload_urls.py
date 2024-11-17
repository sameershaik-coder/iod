import pytest
from django.urls import reverse, resolve
from apps.home import views
from tests.test_classes import BaseTest

@pytest.mark.django_db
class TestViewUploadURL(BaseTest):

    def test_upload_url_resolves(self,client,user):
        """
        Test that the URL for 'view_upload' resolves correctly.
        """
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        
        response = client.get(reverse("view_upload"))

        assert response.status_code == 200
