from django.urls import reverse
import pytest
from tests.test_classes import BaseTest

@pytest.mark.django_db
class Test_Category_Urls(BaseTest):
    
    def test_view_assetgroup_reg_user(self,user,client,networth,base_unit,assetgroup,instrument):
        # initializes client fixture with regular user log in
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        
        response = client.get(reverse("assets", args=[assetgroup.id]))

        assert response.status_code == 200