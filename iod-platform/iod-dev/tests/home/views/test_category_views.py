import pytest
from apps.home.models import AssetGroup, Category, Instrument
from tests.test_classes import BaseTest
from apps.home.lib import (
    common
)
from test_common import(
    get_response_viewname_kwargs,
    assert_response_success
)
@pytest.mark.django_db
class Test_Category_Views(BaseTest):
    
    def test_category_view(self,user,client,networth,base_unit,category,assetgroup,instrument):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)

        total_selected_asset_allocation = category.get_category_allocation() 
        
        response = get_response_viewname_kwargs(client,"category",kwargs={"pk": category.pk})
        assert_response_success(response,"category")
        assert len(response.context["assets"]) == 1
        assert response.context["total_selected_asset_allocation"] == total_selected_asset_allocation
        assert response.context["total_invested_amount"] == common.get_total_asset_invested(category)

    def test_category_view_with_asset_currentvalue_zero(self,user,client,networth,base_unit,category,assetgroup,instrument):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)

        ag_2 = AssetGroup.objects.create(name='Test Ag 2', weightage=20, category=category)
        Instrument.objects.create(name='Test AG 1', amount_invested=10, asset=ag_2)

        total_selected_asset_allocation = category.get_category_allocation() 

        response = get_response_viewname_kwargs(client,"category",kwargs={"pk": category.pk})
        assert_response_success(response,"category")
        assert len(response.context["assets"]) == 2
        assert response.context["total_selected_asset_allocation"] == total_selected_asset_allocation
        assert response.context["total_invested_amount"] == common.get_total_asset_invested(category) 
    
    def test_category_view_with_asset_totalinvestment_zero(self,user,client,networth,base_unit,category,assetgroup,instrument):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)

        #ag_2 = AssetGroup.objects.create(name='Test Ag 2', weightage=20, category=category)
        #Instrument.objects.create(name='Test AG 1', amount_invested=10, asset=ag_2)
        ag = AssetGroup.objects.get(id=assetgroup.id)
        ag.delete()
        total_selected_asset_allocation = category.get_category_allocation() 

        response = get_response_viewname_kwargs(client,"category",kwargs={"pk": category.pk})
        assert_response_success(response,"category")
        assert len(response.context["assets"]) == 0
        assert response.context["total_selected_asset_allocation"] == total_selected_asset_allocation
        assert response.context["total_invested_amount"] == common.get_total_asset_invested(category) 
    
    def test_category_view_with_asset_totalallocation_zero(self,user,client,networth,base_unit,category,assetgroup,instrument):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)

        ag_2 = AssetGroup.objects.create(name='Test Ag 2', weightage=20, category=category)
        ag_2.category = category
        ag_2.save()
        Instrument.objects.create(name='Test AG 1', amount_invested=100000, asset=ag_2)

        # ag = AssetGroup.objects.get(id=assetgroup.id)
        # ag.delete()
        cat = Category.objects.get(id=category.id)
        cat.weightage = 0
        cat.save()
        cat.refresh_from_db()
        total_selected_asset_allocation = 0

        response = get_response_viewname_kwargs(client,"category",kwargs={"pk": category.pk})
        assert_response_success(response,"500")

            
    
    def test_category_view_with_invalid_category(self,user,client,networth,base_unit):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)

        response = get_response_viewname_kwargs(client,"category",kwargs={"pk": 999})
        assert_response_success(response,"500")