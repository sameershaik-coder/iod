
def get_default_asset_type_data():
    data = {
            'name': 'Test Asset Type',
            'weightage': 10
        }
    return data

def set_default_asset_type_data(name, weightage):
    data = {
            'name': name,
            'weightage': weightage
        }
    return data

################################################################################################################################
# Validation
################################################################################################################################
def assert_asset_type(asset_type,data,networth):
    assert asset_type.name == data['name']
    assert asset_type.weightage == data['weightage']
    assert asset_type.networth == networth