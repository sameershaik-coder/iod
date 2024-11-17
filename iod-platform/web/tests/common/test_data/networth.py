from tests.common import utils

def get_default_networth_data():
    data = {
            'name': utils.generate_random_text(10),
            'amount': 10,
            'is_active': False
        }
    return data

def set_default_networth_data(name, amount,is_active):
    data = {
            'name': name,
            'amount': amount,
            'is_active': is_active
        }
    return data

################################################################################################################################
# Validation
################################################################################################################################
def assert_networth(networth,data, user):
    assert networth.name == data['name']
    assert networth.amount == data['amount']
    assert networth.user == user
    assert networth.is_active == data['is_active']