from django.contrib.auth.models import User
from apps.home.models import(
    BaseUnit,
    Networth,
    UserNominee,
)
from django.utils import timezone
from django.test import Client
import pytest
from apps.home.actions import (
     instruments as instruments_actions, 
     networth as networth_actions, category as category_actions, 
     assetgroup as assetgroup_actions,
     baseunit as baseunit_actions,
     assettype as assettype_actions,
     user as user_actions,
     nominee as nominee_actions,
     backup as backup_actions
     
) 

@pytest.mark.django_db
class BaseTest:
    @pytest.fixture
    def user(self):
        country = "IN"
        user = user_actions.do_create_user("Test@mail.com", "Test@123",country,"Test@mail.com")
        yield user
        user.delete()
    
    @pytest.fixture
    def nominee(self,user):
        
        qs = UserNominee.objects.filter(user=user,status="A")
        if len(qs)==1:
            nominee = qs[0]
        else:
            nominee = nominee_actions.do_create_nominee("default nominee","test_nominee@mail.com", user=user)
        yield nominee
        nominee.delete()

 
    @pytest.fixture
    def networth(self,user):
        qs = Networth.objects.get(user=user)
        if qs is None :
            networth = networth_actions.do_create_networth("Test Networth",30,user)
            networth.is_active = True
            networth.save()
        else:
            networth = qs
            networth.amount = 30
            networth.save()
        yield networth
        networth.delete()

    @pytest.fixture
    def base_unit(self,user,networth):
        unit = BaseUnit.objects.get(networth = networth)
        unit.value = 100000
        unit.save()
        yield unit
        unit.delete()

    @pytest.fixture
    def asset_type(self,user,networth):
        asset_type = assettype_actions.do_create_assettype("Test Asset Type",30,user)
        yield asset_type
        asset_type.delete()

    @pytest.fixture
    def category(self,user,networth):
        category = category_actions.do_create_category("MF",25,user)
        yield category
        category.delete()
    
    @pytest.fixture
    def assetgroup(self,user,category):
        assetgroup = assetgroup_actions.do_create_assetgroup("Test AG1",25,category,user)
        yield assetgroup
        assetgroup.delete() 

    @pytest.fixture
    def instrument(self,user,assetgroup):
        instrument = instruments_actions.do_create_instrument("TestInstrument1",25,10000,assetgroup,user,10880)
        yield instrument
        instrument.delete() 
    
    @pytest.fixture
    def backup(self,user):
        backup = backup_actions.do_create_backup2(user,"TestBackup")
        yield backup
        backup.delete()
################################################################################################################################
# Client
################################################################################################################################

    def user_login(self,client,user):
        client.force_login(user)    

################################################################################################################################
# Users
################################################################################################################################

    def initialize_user(self,user:User,is_superuser:bool,is_staff:bool,is_active:bool):
            user.is_superuser = is_superuser
            user.is_staff = is_staff
            user.is_active = is_active
            user.save()

   
    

    