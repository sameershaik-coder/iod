from apps.home.lib import constants
from apps.home.actions.baseunit import get_base_settings_with_country
from apps.home.models import UserProfile

def get_default_base_unit_data():
    data = {
            'name': 'Test Base Unit',
            'value': 10
        }
    return data

def set_default_base_unit_data(name, value):
    data = {
            'name': name,
            'value': value
        }
    return data

################################################################################################################################
# Validation
################################################################################################################################
def assert_base_unit_default(base_unit,networth):
    profile = UserProfile.objects.get(user=networth.user)
    base_settings = get_base_settings_with_country(profile.country)
    assert base_unit.name == base_settings["name"]
    assert base_unit.value == base_settings["value"]
    assert base_unit.networth == networth

def assert_base_unit(base_unit,data,networth):
    assert base_unit.name == data["name"]
    assert base_unit.value == data["value"]
    assert base_unit.networth == networth