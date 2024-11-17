
def get_default_category_data():
    data = {
            'name': 'Test Category',
            'weightage': 10
        }
    return data

def set_default_category_data(name, weightage):
    data = {
            'name': name,
            'weightage': weightage
        }
    return data

################################################################################################################################
# Validation
################################################################################################################################
def assert_category(category,data,networth):
    assert category.name == data['name']
    assert category.weightage == data['weightage']
    assert category.networth == networth