from tests.common import utils

def get_default_userprofile_data():
    data = {
            'first_name': utils.generate_random_text(119),
            'last_name': utils.generate_random_text(119),
            'address': utils.generate_random_text(119),
            'bio': utils.generate_random_text(499)
        }
    return data

def set_default_userprofile_data(first_name, last_name,address,bio):
    data = {
            'first_name': first_name,
            'last_name': last_name,
            'address': address,
            'bio': bio
        }
    return data

################################################################################################################################
# Validation
################################################################################################################################
def assert_userprofile(userprofile,data,user):
    assert userprofile.first_name == data['first_name']
    assert userprofile.last_name == data['last_name']
    assert userprofile.address == data['address']
    assert userprofile.bio == data['bio']
    assert userprofile.user == user