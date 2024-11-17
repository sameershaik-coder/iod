from apps.home.models import(
    BaseUnit,
    Networth,
    UserProfile
    )
from django.contrib.auth.models import User
from typing import Optional
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from apps.home.lib.country import(
    india as India
)
from apps.home.lib import constants

get_base_units_by_user = lambda user: BaseUnit.objects.filter(networth__user = user)

def get_default_baseunit(networth:Networth) -> Optional[BaseUnit]:
    return BaseUnit.objects.get(networth=networth)

def get_base_unit(id, user) -> Optional[BaseUnit]:
    return BaseUnit.objects.get(id = id, networth__user = user)

def do_create_baseunit(name:str,value:int,networth:Networth)-> BaseUnit:
    qs = BaseUnit.objects.filter(networth=networth)
    if len(qs) <= 0:
        with transaction.atomic():
            base_unit = BaseUnit.objects.create(
                name = name,
                value = value,
                networth = networth
            )
            base_unit.save()
        
            return base_unit
    else:
        return qs.first()

def do_create_baseunit_with_user(user:User,networth:Networth)-> BaseUnit:
    qs = BaseUnit.objects.filter(networth=networth)
    profile = UserProfile.objects.get(user=user)
    base_unit = get_base_settings_with_country(profile.country)
    if len(qs) <= 0:
        with transaction.atomic():
            base_unit = BaseUnit.objects.create(
                name = base_unit["name"],
                value = base_unit["value"],
                networth = networth
            )
            base_unit.save()
        
            return base_unit
    else:
        return qs.first()

def get_base_settings_with_country(country:str):
    if country == 'IN':
        return {
            'name' : India.DEFAULT_BASE_UNIT_NAME,
            'value' : India.DEFAULT_BASE_UNIT_VALUE
        }
    else:
        return {
            'name' : constants.DEFAULT_BASE_UNIT_NAME,
            'value' : constants.DEFAULT_BASE_UNIT_VALUE
        }