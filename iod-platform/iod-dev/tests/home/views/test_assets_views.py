import pytest
from apps.home.models import AssetGroup, Instrument, UserProfile
from tests.test_classes import BaseTest
from django.urls import reverse
from apps.home.actions import(
    networth as networth_actions,
    baseunit as baseunit_actions
)
from django.contrib.auth.models import User
from test_common import(
    get_response_viewname_kwargs,
    assert_response_success
)
from apps.home.actions import(
    userprofile as userprofile_actions
)
@pytest.mark.django_db
class Test_Assets_Views(BaseTest):
    def test_assets_view_authenticated_user(self,user,client,networth,base_unit,assetgroup,instrument):
        """
        Test assets view for an authenticated user
        """
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        # Create a request
        response = get_response_viewname_kwargs(client,"assets",kwargs={"pk": assetgroup.pk})
        
        assert_response_success(response,"assets")
        assert str(instrument) in str(response.content)
        assert str(instrument.amount_invested) in str(response.content)
    
    def test_assets_view_with_instrument_currentvalue_zero(self,user,client,networth,base_unit,assetgroup,instrument):
        """
        Test assets view for an authenticated user
        """
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        
        i2 = Instrument.objects.create(name='Test Ins 1', amount_invested=10, asset=assetgroup)

        # Create a request
        response = get_response_viewname_kwargs(client,"assets",kwargs={"pk": assetgroup.pk})

        assert_response_success(response,"assets")
        assert str(i2.name) in str(response.content)
        assert str(i2.amount_invested) in str(response.content)
        assert "0%" in str(response.content)

    def test_assets_view_with_instrument_totalinvestment_zero(self,user,client,networth,base_unit,assetgroup,instrument):
        """
        Test assets view for an authenticated user
        """
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        
        iname = instrument.name
        iamount = instrument.amount_invested

        instrument = Instrument.objects.get(id=instrument.id)
        instrument.delete()

        # Create a request
        response = get_response_viewname_kwargs(client,"assets",kwargs={"pk": assetgroup.pk})
        assert_response_success(response,"assets")
        assert str(iname) not in str(response.content)
        assert str(iamount) not in str(response.content)
        assert "0%" in str(response.content)

    def test_assets_view_unauthenticated_user(self,client,assetgroup):
        """
        Test assets view for an unauthenticated user
        """
        url = reverse('assets',kwargs={"pk": assetgroup.pk})
        response = get_response_viewname_kwargs(client,"assets",kwargs={"pk": assetgroup.pk})
        assert response.status_code == 302
        some1 = response.url
        some2 = reverse('login') + '?next=' + url
        assert response.url == '/login/?next=' + url
    
    def test_assets_view_with_invalid_asset_group_pk(self,client,user):
        """
        Test assets view with an invalid asset group pk
        """
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        response = get_response_viewname_kwargs(client,"assets",kwargs={"pk": 9999})
        assert_response_success(response,"500")

    # def test_assets_view_with_permission_denied(self,client,user,assetgroup):
    #     """
    #     Test assets view with permission denied
    #     """
    #     # Create a user without permission to view assets
    #     user_without_permission = User.objects.create_user(username='testuser2', password='testpassword2')
    #     userprofile_actions.do_create_user_profile(user_without_permission,country="IN")
    #     other_networth = networth_actions.do_create_networth("Test Networth",30,user_without_permission)
    #     other_networth.is_active = True
    #     other_networth.save()
        
    #     self.user_login(client,user_without_permission)
        
    #     response = get_response_viewname_kwargs(client,"assets",kwargs={"pk": assetgroup.id})

    #     assert_response_success(response,"404")





