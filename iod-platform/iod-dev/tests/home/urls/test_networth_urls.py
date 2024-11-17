from django.urls import reverse
import pytest
from tests.test_classes import BaseTest

################################################################################################################################
# Networth
################################################################################################################################

@pytest.mark.django_db
class Test_Networth_Urls(BaseTest):

    def test_view_networth_reg_user(self,user,client,networth):
        # initializes client fixture with regular user log in
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)
        response = client.get(reverse("networth"))

        assert response.status_code == 200