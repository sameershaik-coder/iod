import pytest
from tests.test_classes import BaseTest
from test_common import (
    assert_response_success,
)

################################################################################################################################
# Support pages
################################################################################################################################

@pytest.mark.django_db
class Test_Support_Views(BaseTest):
    def test_support_pages_view(self,user,client,networth,base_unit,assetgroup,instrument):
        """
        pages support
        """
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        # Create a request
        url = "/app/support"
        response = client.get(url)
        assert_response_success(response,"support")

################################################################################################################################
# Demo pages
################################################################################################################################
@pytest.mark.django_db
class Test_Demo_Views(BaseTest):
    def test_demo_pages_view(self,user,client,networth,base_unit,assetgroup,instrument):
        """
        pages demo
        """
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        # Create a request
        url = "/app/demo"
        response = client.get(url)
        assert_response_success(response,"demo")