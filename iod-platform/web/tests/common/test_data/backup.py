from apps.home.actions import backup as backup_actions


def get_default_backup_data():
    data = {
            'name': 'Test Backup'
        }
    return data

def set_default_backup_data(name):
    data = {
            'name': name
        }
    return data

################################################################################################################################
# Validation
################################################################################################################################
def assert_backup(backup,user,name):
    assert backup.name == name
    assert backup.user == user
