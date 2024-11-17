import pytest
from tests.test_classes import BaseTest
from django.contrib.auth.models import User
from apps.home.actions import assetgroup as assetgroup_actions 
from apps.home.models import (
    BaseUnit,
    Networth,
    Category,
    AssetGroup,
    Instrument
)
from django.core.exceptions import ObjectDoesNotExist,ValidationError
from apps.home.lib.exceptions import JsonableError
from apps.home.actions import instruments as instruments_actions, networth as networth_actions

################################################################################################################################
# Instrument
################################################################################################################################
@pytest.mark.django_db
class Test_Instrument_Models(BaseTest):
    def test_instrument_allocation_base_unit_invalid(self,user,base_unit,assetgroup)->None:
        
        i1 = instruments_actions.do_create_instrument("TestInstrument1",25,10000,assetgroup,user)

        base_unit.value = -1
        base_unit.save()
        base_unit.refresh_from_db()
        assert i1.get_instrument_allocation() == 1
    
    def test_instrument_invalid_instrument_exists(self,user,assetgroup)->None:
        i1 = instruments_actions.do_create_instrument("TestInstrument1",25,10000,assetgroup,user)
        with pytest.raises(JsonableError) as exc_info:
            instruments_actions.do_create_instrument("TestInstrument1",20,10000,assetgroup,user)
            
        assert str(exc_info.value) == "Instrument already exists for given name and assetgroup combination"

################################################################################################################################
# Instrument Weightage
################################################################################################################################
class Test_AssetGroup_Weightage(BaseTest):

    def test_do_multiple_instrument_weightage_hundred(self,user,assetgroup)->None:

        i1 = instruments_actions.do_create_instrument("TestInstrument1",25,10000,assetgroup,user)
        i2 = instruments_actions.do_create_instrument("TestInstrument2",25,10000,assetgroup,user)
        i3 = instruments_actions.do_create_instrument("TestInstrument3",25,10000,assetgroup,user)
        i4 = instruments_actions.do_create_instrument("TestInstrument4",25,10000,assetgroup,user)

        assert Instrument.objects.get(name="TestInstrument1")==i1
        assert Instrument.objects.get(name="TestInstrument2")==i2
        assert Instrument.objects.get(name="TestInstrument3")==i3
        assert Instrument.objects.get(name="TestInstrument4")==i4

    def test_do_multiple_instrument_weightage_lessthan_hundred(self,user,assetgroup)->None:
        i1 = instruments_actions.do_create_instrument("TestInstrument1",25,10000,assetgroup,user)
        i2 = instruments_actions.do_create_instrument("TestInstrument2",25,10000,assetgroup,user)
        i3 = instruments_actions.do_create_instrument("TestInstrument3",25,10000,assetgroup,user)
        i4 = instruments_actions.do_create_instrument("TestInstrument4",24.99,10000,assetgroup,user)

        assert Instrument.objects.get(name="TestInstrument1")==i1
        assert Instrument.objects.get(name="TestInstrument2")==i2
        assert Instrument.objects.get(name="TestInstrument3")==i3
        assert Instrument.objects.get(name="TestInstrument4")==i4

    def test_do_multiple_instrument_weightage_morethan_hundred(self,user,assetgroup)->None:
        i1 = instruments_actions.do_create_instrument("TestInstrument1",25,10000,assetgroup,user)
        i2 = instruments_actions.do_create_instrument("TestInstrument2",25,10000,assetgroup,user)
        i3 = instruments_actions.do_create_instrument("TestInstrument3",25,10000,assetgroup,user)
        with pytest.raises(JsonableError):
            instruments_actions.do_create_instrument("TestInstrument4",25.10,10000,assetgroup,user)

        assert Instrument.objects.filter(name="Test AG4").count()==0

        i4 = instruments_actions.do_create_instrument("TestInstrument4",25,10000,assetgroup,user)

        with pytest.raises(JsonableError):
            instruments_actions.do_create_instrument("TestInstrument5",1,10000,assetgroup,user)

        assert Instrument.objects.filter(name="TestInstrument5").count()==0

# ################################################################################################################################
# # Create Instrument
# ################################################################################################################################
class Test_Instrument_Create(BaseTest):
    @pytest.mark.parametrize("user_types", ["customer_user", "staff_user", "admin_user"])
    def test_do_create_instrument_user_with_perm(self,user_types,category,assetgroup,user,base_unit,networth)->None:
        # update user based on scenario
        if user_types == "customer_user":
            self.initialize_user(user,False,False,True)
        elif user_types == "staff_user":
            self.initialize_user(user,False,True,True)
        elif user_types == "admin_user":
            self.initialize_user(user,True,False,True)

        i1 = instruments_actions.do_create_instrument("TestInstrument1",20,10000,assetgroup,user)
        
        instrument1 = Instrument.objects.get(name="TestInstrument1")
        
        assert instrument1.asset.category.networth.user==user
        assert instrument1.asset.category.networth.baseunit==base_unit
        assert instrument1.asset.category.networth== networth
        assert instrument1.asset.category== category
        assert instrument1.asset== assetgroup
        assert instrument1.name== "TestInstrument1"
        assert instrument1.weightage== 20
        assert instrument1.amount_invested== 10000

    @pytest.mark.parametrize("user_types", ["customer_user", "staff_user", "admin_user"])
    def test_do_create_instrument_user_without_perm(self,user_types,user,assetgroup)->None:
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
            instruments_actions.do_create_instrument("TestInstrument1",20,10000,assetgroup,other_user)

        assert Instrument.objects.filter(name="TestInstrument1").count() == 0

            
################################################################################################################################
# Delete Instrument
################################################################################################################################

class Test_Instrument_Delete(BaseTest):
    @pytest.mark.parametrize("user_types", ["customer_user", "staff_user", "admin_user"])
    def test_do_delete_agroup_user_with_perm(self,user_types,user,assetgroup)->None:
        # update user based on scenario
        if user_types == "customer_user":
            self.initialize_user(user,False,False,True)
        elif user_types == "staff_user":
            self.initialize_user(user,False,True,True)
        elif user_types == "admin_user":
            self.initialize_user(user,True,False,True)

        instruments_actions.do_create_instrument("TestInstrument1",20,10000,assetgroup,user)
        
        instrument1 = Instrument.objects.get(name="TestInstrument1")

        instruments_actions.do_delete_instrument(instrument1,acting_user=user)

        assert Instrument.objects.filter(name="TestInstrument1").count() == 0
    
    @pytest.mark.parametrize("user_types", ["customer_user", "staff_user", "admin_user"])
    def test_do_delete_agroup_user_without_perm(self,user_types,user,assetgroup)->None:
        # update user based on scenario
        if user_types == "customer_user":
            self.initialize_user(user,False,False,True)
        elif user_types == "staff_user":
            self.initialize_user(user,False,True,True)
        elif user_types == "admin_user":
            self.initialize_user(user,True,False,True)

        instrument1 = instruments_actions.do_create_instrument("TestInstrument1",20,10000,assetgroup,user)

        other_user = User.objects.create_user(username='other_user', password='password')
        with pytest.raises(JsonableError):
            instruments_actions.do_delete_instrument(instrument1,acting_user=other_user)

        assert Instrument.objects.filter(name="TestInstrument1").count() == 1

    def test_do_delete_parent_verify_asset_deleted(self,user,assetgroup)->None:
        ag1 = instruments_actions.do_create_instrument("TestInstrument1",20,10000,assetgroup,user)
        ag1.delete()
        
        assert Instrument.objects.filter(name="TestInstrument1").count() == 0



                
