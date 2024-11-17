import pytest
from tests.test_classes import BaseTest
from django.contrib.auth.models import User
from apps.home.actions import instruments, networth, category, assetgroup
from apps.home.models import (
    BaseUnit,
    Networth,
    Category,
    AssetGroup,
    Instrument
)
from django.core.exceptions import ObjectDoesNotExist,ValidationError
from apps.home.lib.exceptions import JsonableError
from apps.home.actions import instruments, networth as networth_actions

################################################################################################################################
# AssetGroup
################################################################################################################################
@pytest.mark.django_db
class Test_AssetGroup_Models(BaseTest):
    def test_category_allocation_base_unit_invalid(self,user,base_unit,category)->None:
        
        assetgroup1 = assetgroup.do_create_assetgroup("Test AG1",25,category,user)

        base_unit.value = -1
        base_unit.save()
        assert assetgroup1.get_asset_allocation() == 1

################################################################################################################################
# AssetGroup Weightage
################################################################################################################################
class Test_AssetGroup_Weightage(BaseTest):

    def test_do_multiple_agroups_weightage_hundred(self,user,category)->None:
        a1 = assetgroup.do_create_assetgroup("Test AG1",25,category,user)
        a2 = assetgroup.do_create_assetgroup("Test AG2",25,category,user)
        a3 = assetgroup.do_create_assetgroup("Test AG3",25,category,user)
        a4 = assetgroup.do_create_assetgroup("Test AG4",25,category,user)

        assert AssetGroup.objects.get(name="Test AG1")==a1
        assert AssetGroup.objects.get(name="Test AG2")==a2
        assert AssetGroup.objects.get(name="Test AG3")==a3
        assert AssetGroup.objects.get(name="Test AG4")==a4

    def test_do_multiple_agroups_weightage_lessthan_hundred(self,user,category)->None:
        a1 = assetgroup.do_create_assetgroup("Test AG1",20,category,user)
        a2 = assetgroup.do_create_assetgroup("Test AG2",20,category,user)
        a3 = assetgroup.do_create_assetgroup("Test AG3",20,category,user)
        a4 = assetgroup.do_create_assetgroup("Test AG4",39,category,user)

        assert AssetGroup.objects.get(name="Test AG1")==a1
        assert AssetGroup.objects.get(name="Test AG2")==a2
        assert AssetGroup.objects.get(name="Test AG3")==a3
        assert AssetGroup.objects.get(name="Test AG4")==a4

    def test_do_multiple_agroups_weightage_morethan_hundred(self,user,category)->None:
        a1 = assetgroup.do_create_assetgroup("Test AG1",20,category,user)
        a2 = assetgroup.do_create_assetgroup("Test AG2",20,category,user)
        a3 = assetgroup.do_create_assetgroup("Test AG3",20,category,user)

        with pytest.raises(JsonableError):
            assetgroup.do_create_assetgroup("Test AG4",41,category,user)

        assert AssetGroup.objects.filter(name="Test AG4").count()==0

        a4 = assetgroup.do_create_assetgroup("Test Ag4",40,category,user)

        with pytest.raises(JsonableError):
            assetgroup.do_create_assetgroup("Test Ag5",1,category,user)

        assert AssetGroup.objects.filter(name="Test Ag5").count()==0

################################################################################################################################
# Create AssetGroup
################################################################################################################################
class Test_AssetGroup_Create(BaseTest):

    def test_do_create_agroup_invalid_already_exists(self,user,category)->None:
        self.initialize_user(user,False,False,True)
        assetgroup1 = assetgroup.do_create_assetgroup("Test AG1",25,category,user)
        with pytest.raises(JsonableError) as exc_info:
            assetgroup.do_create_assetgroup("Test AG1",20,category,user)
        assert str(exc_info.value) == "Asset Group already exists for given name and category combination"

    @pytest.mark.parametrize("user_types", ["customer_user", "staff_user", "admin_user"])
    def test_do_create_agroup_user_with_perm(self,user_types,category,user,base_unit,networth)->None:
        # update user based on scenario
        if user_types == "customer_user":
            self.initialize_user(user,False,False,True)
        elif user_types == "staff_user":
            self.initialize_user(user,False,True,True)
        elif user_types == "admin_user":
            self.initialize_user(user,True,False,True)

        assetgroup1 = assetgroup.do_create_assetgroup("Test AG1",25,category,user)
        
        a1 = AssetGroup.objects.get(name="Test AG1")
        
        assert a1.category.networth.user==user
        assert a1.category.networth.baseunit==base_unit
        assert a1.category.networth==networth
        assert a1.category==category
        assert a1 == assetgroup1
        assert a1.name == "Test AG1"
        assert a1.weightage==25

    @pytest.mark.parametrize("user_types", ["customer_user", "staff_user", "admin_user"])
    def test_do_create_agroup_user_without_perm(self,user_types,user,category)->None:
        # update user based on scenario
        if user_types == "customer_user":
            self.initialize_user(user,False,False,True)
        elif user_types == "staff_user":
            self.initialize_user(user,False,True,True)
        elif user_types == "admin_user":
            self.initialize_user(user,True,False,True)

        # create a different user other than user mapped with the category
        other_user = User.objects.create_user(username='other_user', password='password')
        
        with pytest.raises(JsonableError):
            assetgroup.do_create_assetgroup("Test AG1",20,category,other_user)

        assert AssetGroup.objects.filter(name="Test AG1").count()==0

            


################################################################################################################################
# Delete Instrument
################################################################################################################################

class Test_AssetGroup_Delete(BaseTest):
    @pytest.mark.parametrize("user_types", ["customer_user", "staff_user", "admin_user"])
    def test_do_delete_agroup_user_with_perm(self,user_types,user,category)->None:
        # update user based on scenario
        if user_types == "customer_user":
            self.initialize_user(user,False,False,True)
        elif user_types == "staff_user":
            self.initialize_user(user,False,True,True)
        elif user_types == "admin_user":
            self.initialize_user(user,True,False,True)

        assetgroup1 = assetgroup.do_create_assetgroup("Test AG1",25,category,user)

        assetgroup.do_delete_asset(assetgroup1,acting_user=user)

        qs = AssetGroup.objects.filter(name="Test AG1")
        assert qs.count()==0
    
    @pytest.mark.parametrize("user_types", ["customer_user", "staff_user", "admin_user"])
    def test_do_delete_agroup_user_without_perm(self,user_types,user,category)->None:
        # update user based on scenario
        if user_types == "customer_user":
            self.initialize_user(user,False,False,True)
        elif user_types == "staff_user":
            self.initialize_user(user,False,True,True)
        elif user_types == "admin_user":
            self.initialize_user(user,True,False,True)

        assetgroup1 = assetgroup.do_create_assetgroup("Test AG1",25,category,user)

        other_user = User.objects.create_user(username='other_user', password='password')
        with pytest.raises(JsonableError):
            assetgroup.do_delete_asset(assetgroup1,acting_user=other_user)

        qs = AssetGroup.objects.filter(name="Test AG1")
        assert qs.count()==1

    def test_do_delete_parent_verify_asset_deleted(self,user,category)->None:
        ag1 = assetgroup.do_create_assetgroup("Test AG1",25,category,user)
        ag1.delete()
        qs = AssetGroup.objects.filter(name="Test AG1")

        assert qs.count()==0



                
