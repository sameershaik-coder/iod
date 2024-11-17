from tests.common import utils

def get_default_nominee_data():
    data = {
            'name': utils.generate_random_text(119),
            'email': utils.generate_random_email(),
            'status': "A"
        }
    return data

def set_default_nominee_data(name, email,status):
    data = {
            'name': name,
            'email': email,
            'status': status
        }
    return data

################################################################################################################################
# Validation
################################################################################################################################
def assert_nominee(nominee,data,user):
    assert nominee.name == data['name']
    assert nominee.email == data['email']
    assert nominee.status == data['status']
    assert nominee.user == user