from django.urls import reverse
import pytest
from tests.test_classes import BaseTest

@pytest.mark.django_db
class Test_Category_Urls(BaseTest):
    
    def test_view_category_reg_user(self,user,client,networth,base_unit,category):
        # initializes client fixture with regular user log in
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)
        response = client.get(reverse("category", args=[category.id]))

        assert response.status_code == 200