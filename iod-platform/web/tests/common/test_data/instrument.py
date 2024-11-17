
def get_default_instrument_data():
    data = {
            'name': 'Test Asset-Group',
            'amount_invested': 1000000,
            'current_value' : 1100000
        }
    return data

def set_default_instrument_data(name, amount_invested,current_value):
    data = {
            'name': name,
            'amount_invested': amount_invested,
            'current_value' : current_value
        }
    return data

################################################################################################################################
# Validation
################################################################################################################################
def assert_instrument(instrument,assetgroup,data):
    assert instrument.name == data['name']
    assert instrument.amount_invested == data['amount_invested']
    assert instrument.current_value == data['current_value']
    assert instrument.asset == assetgroup