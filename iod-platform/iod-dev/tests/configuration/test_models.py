import pytest
from tests.test_classes import BaseTest
from apps.configuration.models import(
    AssetType
)
from apps.home.models import(
    BaseUnit,
    Networth,
)
from apps.home.actions import(
    networth as networth_actions,
    baseunit as baseunit_actions
)

################################################################################################################################
# AssetType
################################################################################################################################

@pytest.mark.django_db
class Test_AssetType_Models(BaseTest):

    def test_create_asset_type_model_2(self,user,networth):
        self.initialize_user(user,False,False,True)
        asset_type = AssetType.objects.create(name='Test Asset Type', weightage=5, networth=networth)
        
        assert asset_type.id is not None
        assert asset_type.name == 'Test Asset Type'
        assert asset_type.weightage == 5
        assert asset_type.networth == networth
    
    def test_update_asset_type(self,user,asset_type):
        self.initialize_user(user,False,False,True)
        asset_type.name = 'Updated Asset Type'
        asset_type.weightage = 10
        asset_type.save()
        updated_asset_type = AssetType.objects.get(id=asset_type.id)

        assert updated_asset_type.name == 'Updated Asset Type'
        assert updated_asset_type.weightage == 10

    def test_delete_asset_type(self,user,networth):
        # do not use pytest fixture asset_type here, because it will cause error during cleanup of asset type
        self.initialize_user(user,False,False,True)
        asset_type = AssetType.objects.create(name='Test Asset Type', weightage=5, networth=networth)
        id = asset_type.id
        asset_type.delete()

        assert not AssetType.objects.filter(id=id).exists()

    def test_asset_type_str(self,user,networth):
        self.initialize_user(user,False,False,True)
        asset_type = AssetType.objects.create(name='Test Asset Type', weightage=5, networth=networth)

        assert str(asset_type) == 'Test Asset Type'

################################################################################################################################
# BaseUnit
################################################################################################################################
@pytest.mark.django_db
class Test_BaseUnit_Models(BaseTest):

    def test_create_base_unit_model(self,user):
        self.initialize_user(user,False,False,True)
        networth = Networth.objects.create(name="some networth",amount=32,user=user)
        networth.is_active = True
        networth.save()
        base_unit = baseunit_actions.do_create_baseunit(name='Test Unit', value=5,networth=networth)

        assert base_unit.id is not None
        assert base_unit.name == 'Test Unit'
        assert base_unit.value == 5
        assert base_unit.networth == networth
        

    def test_update_base_unit(self,user,base_unit):
        self.initialize_user(user,False,False,True)
        base_unit.name = 'Updated Asset Type'
        base_unit.value = 10
        base_unit.save()
        updated_base_unit = BaseUnit.objects.get(id=base_unit.id)

        assert updated_base_unit.name == 'Updated Asset Type'
        assert updated_base_unit.value == 10

    def test_delete_base_unit(self,user,networth,base_unit):
        self.initialize_user(user,False,False,True)
        networth.user = user
        base_unit.networth = networth
        base_unit.save()
        updated_base_unit = BaseUnit.objects.get(id=base_unit.id)
        updated_base_unit.delete()

        assert not BaseUnit.objects.filter(id=updated_base_unit.id).exists()

    def test_base_unit_str(self,user):
        self.initialize_user(user,False,False,True)
        networth = Networth.objects.create(name="some networth",amount=32,user=user)
        networth.is_active = True
        networth.save()
        base_unit = baseunit_actions.do_create_baseunit(name='Test Unit', value=5,networth=networth)

        assert str(base_unit) == 'Test Unit'

################################################################################################################################
# Networth
################################################################################################################################
@pytest.mark.django_db
class TestNetworthModels(BaseTest):
    def test_create_networth_model(self, user):
        networth = Networth.objects.create(name='Test Networth', amount=1000, user=user, is_active=True)

        assert networth.id is not None
        assert networth.name == 'Test Networth'
        assert networth.amount == 1000
        assert networth.user == user
        assert networth.is_active is True

    def test_update_networth_model(self, user, networth):
        networth.name = 'Updated Networth'
        networth.amount = 2000
        networth.is_active = False
        networth.save()
        updated_networth = Networth.objects.get(id=networth.id)

        assert updated_networth.name == 'Updated Networth'
        assert updated_networth.amount == 2000
        assert updated_networth.is_active is False

    def test_delete_networth_model(self, user):
        networth = Networth.objects.create(name='Test Networth', amount=1000, user=user, is_active=True)
        id = networth.id
        networth.delete()

        assert not Networth.objects.filter(id=id).exists()

    def test_networth_str(self, user):
        networth = Networth.objects.create(name='Test Networth', amount=1000, user=user, is_active=True)

        assert str(networth) == 'Test Networth'
