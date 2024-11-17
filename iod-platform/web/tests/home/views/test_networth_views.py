import pytest
from tests.test_classes import BaseTest
from django.urls import reverse
from test_common import (
    get_response_using_view_name,
    assert_response_success,
    assert_data_in_context
)
from django.contrib.auth.models import User
@pytest.mark.django_db
class Test_Networth_Views(BaseTest):
    def test_networth_view_authenticated_user(self,client,user,networth,base_unit,category,assetgroup,instrument):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        response = get_response_using_view_name(client,"networth")
        assert_response_success(response,'networth')
        assert_data_in_context(response,['total_networth_amount','category_list','total_invested_amount'])
    
    def test_networth_view_with_category_zero_weightage(self,client,user,networth,base_unit,category,assetgroup,instrument):
        self.initialize_user(user,False,False,True)
        category.weightage = 0
        category.save()
        category.refresh_from_db()
        self.user_login(client,user)
        response = get_response_using_view_name(client,"networth")
        assert_response_success(response,'networth')
        assert_data_in_context(response,['total_networth_amount','category_list','total_invested_amount'])

    def test_networth_view_raise_exception(self,client,user):
        other_user = User.objects.create_user(username='other_user', password='password')
        self.user_login(client,other_user)
        other_user.email = user.email
        other_user.save()
        response = get_response_using_view_name(client,"networth")
        assert_response_success(response,"500")


    def test_networth_view_unauthenticated_user(self,client):
        url = reverse('networth')
        response = client.get(url)
        assert response.status_code == 302
        assert response.url == '/login/?next=' + url
