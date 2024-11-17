
def get_default_asset_group_data():
    data = {
            'name': 'Test Asset-Group',
            'weightage': 10
        }
    return data

def set_default_asset_group_data(name, weightage):
    data = {
            'name': name,
            'weightage': weightage
        }
    return data

################################################################################################################################
# Validation
################################################################################################################################
def assert_asset_group(asset_group,data,category):
    assert asset_group.name == data['name']
    assert asset_group.weightage == data['weightage']
    assert asset_group.category == category