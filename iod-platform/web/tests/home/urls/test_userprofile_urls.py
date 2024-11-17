from django.urls import reverse
import pytest
from tests.test_classes import BaseTest

################################################################################################################################
# Networth
################################################################################################################################

@pytest.mark.django_db
class Test_UserProfile_Urls(BaseTest):
    @pytest.mark.parametrize("user_types", ["customer_user", "staff_user", "admin_user"])
    def test_view_userprofile_reg_user(self,user_types,user,client):
        if user_types == "customer_user":
            self.initialize_user(user,False,False,True)
        elif user_types == "staff_user":
            self.initialize_user(user,False,True,True)
        elif user_types == "admin_user":
            self.initialize_user(user,True,False,True)

        self.user_login(client, user)
        response = client.get(reverse("view_profile"))

        assert response.status_code == 200