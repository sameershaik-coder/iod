from django.urls import reverse
from django.shortcuts import redirect
import pytest
from tests.test_classes import BaseTest

################################################################################################################################
# Instrument
################################################################################################################################
@pytest.mark.django_db
class Test_Instrument_Urls(BaseTest):

    def test_view_instrument_reg_user(self,user,client,networth,category,assetgroup,instrument):
        # initializes client fixture with regular user log in
        self.initialize_user(user,False,False,True)
        networth.user = user
        self.user_login(client, user)
        response = client.get(reverse("view_instruments",kwargs={'category_id': category.id,'asset_group_id' : assetgroup.id}))

        assert response.status_code == 200

    def test_edit_instrument_reg_user(self,user,client,category,assetgroup,instrument):
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)
        response = client.get(reverse("edit_instrument", kwargs={'category_id': category.id,'asset_group_id':assetgroup.id,
                                                                  'instrument_id' : instrument.id}))

        assert response.status_code == 200

    # def test_delete_category_reg_user(self,user,client,category,assetgroup):
    #     self.initialize_user(user,False,False,True)
    #     self.user_login(client, user)
    #     response = client.get(reverse("delete_asset_group", kwargs={'category_id': category.id,'asset_group_id':assetgroup.id}))

    #     # Delete asset type does not have a page so expecting 302
    #     assert response.status_code == 302
    
    # def test_create_asset_group_reg_user(self,user, client,category):
    #     self.initialize_user(user,False,False,True)
    #     self.user_login(client, user)
    #     response = client.get(reverse("create_asset_group",kwargs={'category_id': category.id}))

    #     assert response.status_code == 200


################################################################################################################################
# Asset-Group
################################################################################################################################
@pytest.mark.django_db
class Test_Asset_Groups_Urls(BaseTest):

    def test_view_ag_reg_user(self,user,client,networth,category,assetgroup):
        # initializes client fixture with regular user log in
        self.initialize_user(user,False,False,True)
        networth.user = user
        self.user_login(client, user)
        response = client.get(reverse("view_asset_groups",kwargs={'category_id': category.id}))

        assert response.status_code == 200

    def test_edit_ag_reg_user(self,user,client,category,assetgroup):
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)
        response = client.get(reverse("edit_asset_group", kwargs={'category_id': category.id,'asset_group_id':assetgroup.id}))

        assert response.status_code == 200

    def test_delete_category_reg_user(self,user,client,category,assetgroup):
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)
        response = client.get(reverse("delete_asset_group", kwargs={'category_id': category.id,'asset_group_id':assetgroup.id}))

        # Delete asset type does not have a page so expecting 302
        assert response.status_code == 302
    
    def test_create_asset_group_reg_user(self,user, client,category):
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)
        response = client.get(reverse("create_asset_group",kwargs={'category_id': category.id}))

        assert response.status_code == 200
################################################################################################################################
# Category
################################################################################################################################

@pytest.mark.django_db
class Test_Category_Urls(BaseTest):

    def test_view_category_reg_user(self,user,client,networth):
        # initializes client fixture with regular user log in
        self.initialize_user(user,False,False,True)
        networth.user = user
        self.user_login(client, user)
        response = client.get(reverse("view_networth"))

        assert response.status_code == 200
    
    def test_edit_category_reg_user(self,user,client,category):
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)
        response = client.get(reverse("edit_category", args=[category.id]))

        assert response.status_code == 200

    def test_delete_category_reg_user(self,user,client,category):
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)
        response = client.get(reverse("delete_category", args=[category.id]))

        # Delete asset type does not have a page so expecting 302
        assert response.status_code == 302

    
    def test_create_category_reg_user(self,user, client):
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)
        response = client.get(reverse("create_category"))

        assert response.status_code == 200

################################################################################################################################
# AssetType
################################################################################################################################

@pytest.mark.django_db
class Test_AssetType_Urls(BaseTest):

    def test_view_asset_types_reg_user(self,user,client,networth):
        # initializes client fixture with regular user log in
        self.initialize_user(user,False,False,True)
        networth.user = user
        self.user_login(client, user)
        response = client.get(reverse("view_asset_types"))

        assert response.status_code == 200
    
    def test_edit_asset_type_reg_user(self,user,client,asset_type):
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)
        response = client.get(reverse("edit_asset_type", args=[asset_type.id]))

        assert response.status_code == 200

    def test_delete_asset_type_reg_user(self,user,client,asset_type):
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)
        response = client.get(reverse("delete_asset_type", args=[asset_type.id]))

        # Delete asset type does not have a page so expecting 302
        assert response.status_code == 302

    
    def test_create_asset_type_reg_user(self,user, client):
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)
        response = client.get(reverse("create_asset_type"))

        assert response.status_code == 200


################################################################################################################################
# BaseUnit
################################################################################################################################
@pytest.mark.django_db
class Test_BaseUnit_Urls(BaseTest):

    def test_view_base_unit_reg_user(self,user,client):
        # initializes client fixture with regular user log in
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)
        response = client.get(reverse("view_base_unit"))

        assert response.status_code == 200

    def test_edit_base_unit_reg_user(self,user,client,base_unit):
        self.initialize_user(user,False,False,True)
        self.user_login(client, user)
        response = client.get(reverse("edit_base_unit", args=[base_unit.id]))

        assert response.status_code == 200
    
    # def test_delete_base_unit_reg_user(self,user,client,base_unit):
    #     self.initialize_user(user,False,False,True)
    #     self.user_login(client, user)
    #     response = client.get(reverse("delete_base_unit", args=[base_unit.id]))

    #     # Delete asset type does not have a page so expecting 302
    #     assert response.status_code == 302

################################################################################################################################
# Networth
################################################################################################################################

@pytest.mark.django_db
class TestNetworthUrls(BaseTest):
    def test_view_networth_reg_user(self, user, client, networth):
        # Initialize client fixture with regular user login
        self.initialize_user(user, False, False, True)
        networth.user = user
        self.user_login(client, user)
        response = client.get(reverse("view_networth"))

        assert response.status_code == 200

    def test_edit_networth_reg_user(self, user, client, networth):
        self.initialize_user(user, False, False, True)
        self.user_login(client, user)
        response = client.get(reverse("edit_networth", args=[networth.id]))

        assert response.status_code == 200

