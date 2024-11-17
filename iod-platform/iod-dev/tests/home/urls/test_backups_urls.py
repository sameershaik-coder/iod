from django.urls import reverse
import pytest
from tests.test_classes import BaseTest

@pytest.mark.django_db
class Test_Backups_Urls(BaseTest):
    
    def test_view_backups_reg_user(self,user,client):
        # initializes client fixture with regular user log in
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        
        response = client.get(reverse("view_backups"))

        assert response.status_code == 200
    
    