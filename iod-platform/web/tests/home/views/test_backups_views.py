import time
import pytest
from unittest.mock import patch
from apps.home.models import AssetGroup, BaseUnit, Instrument, UserProfile
from tests.common.utils import generate_invalid_text, generate_random_text
from tests.test_classes import BaseTest
from django.urls import reverse
from apps.home.actions import(
    networth as networth_actions,
    baseunit as baseunit_actions,
    backup as backup_actions
)
from django.contrib.auth.models import User
from test_common import(
    assert_data_in_context,
    assert_data_not_in_context,
    create_test_data_for_user,
    get_response_using_view_name,
    get_response_viewname_kwargs,
    assert_response_success,
    post_response_using_params,
    post_response_using_view_name,
    validate_response
)
from apps.home.actions import(
    userprofile as userprofile_actions
)
from apps.home.actions import(
    networth as networth_actions,
    baseunit as baseunit_actions,
    category as category_actions,
    assetgroup as ag_actions,
    instruments as instuments_actions,
    userprofile as up_actions,
)
from apps.home.models import (
    Networth,
    Category,
    AssetGroup,
    Instrument,
    Backup,
    NetworthBackup,
    CategoryBackup,
    AssetGroupBackup,
    InstrumentBackup,
    BaseUnitBackup
)
from tests.common.test_data import backup as backup_testdata
from apps.home.lib import (
    backups as backups_lib
)
@pytest.mark.django_db
class Test_Backups_Views(BaseTest):
    AVG_WAIT_TIME = 5

    def create_test_data_for_advanced_for_user(self,user,networth_name,category_name1,category_name2,ag_name1,ag_name2,i1_name,i2_name,i3_name,i4_name,i5_name,i6_name):
        networth = networth_actions.do_create_networth(networth_name,32,user)
        baseunit = baseunit_actions.do_create_baseunit_with_user(user,networth)
        category1 = category_actions.do_create_category(category_name1,50,user)
        ag1 = ag_actions.do_create_assetgroup(ag_name1,50,category1,acting_user=user)
        i1 = instuments_actions.do_create_instrument(name=i1_name,weightage=10,amount_invested=10000,asset=ag1, acting_user=user,current_value=12000)
        i2 = instuments_actions.do_create_instrument(name=i2_name,weightage=10,amount_invested=10000,asset=ag1, acting_user=user,current_value=13000)
        i3 = instuments_actions.do_create_instrument(name=i3_name,weightage=10,amount_invested=10000,asset=ag1, acting_user=user,current_value=7000)

        category2 = category_actions.do_create_category(category_name2,50,user)
        ag2 = ag_actions.do_create_assetgroup(ag_name2,50,category2,acting_user=user)
        i4 = instuments_actions.do_create_instrument(name=i4_name,weightage=10,amount_invested=10000,asset=ag2, acting_user=user,current_value=12000)
        i5 = instuments_actions.do_create_instrument(name=i5_name,weightage=10,amount_invested=10000,asset=ag2, acting_user=user,current_value=13000)
        i6 = instuments_actions.do_create_instrument(name=i6_name,weightage=10,amount_invested=10000,asset=ag2, acting_user=user,current_value=7000)

        backup_name = generate_random_text(10)
        backup_actions.do_create_backup(user,backup_name)
        backup_object = backup_actions.get_backup_by_name(user,backup_name)
        return backup_object

################################################################################################################################
# Restore Backup Tests
################################################################################################################################
    
    def test_backups_restore_raise_exception(self,user,client,mocker):
        mocker.patch.object(backups_lib, 'fetch_post_response_restore', side_effect=Exception("Simulated error"))
        user = User.objects.create_user("sam@mail.com","sam@mail.com","Test@123")
        up_actions.do_create_user_profile(user,country="IN")
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)

        networth_name=generate_random_text(10)
        category_name1=generate_random_text(10)
        category_name2=generate_random_text(10)
        ag_name1=generate_random_text(10)
        ag_name2=generate_random_text(10)
        i1_name=generate_random_text(10)
        i2_name=generate_random_text(10)
        i3_name=generate_random_text(10)
        i4_name=generate_random_text(10)
        i5_name=generate_random_text(10)
        i6_name=generate_random_text(10)


        backup_object = self.create_test_data_for_advanced_for_user(user,networth_name,category_name1,category_name2,ag_name1,ag_name2,i1_name,i2_name,i3_name,i4_name,i5_name,i6_name)

        # make a get request to the restore backup page
        response = client.get(reverse("restore_backup", args=[backup_object.id]))
        # Check that the response status code is 500
        assert_response_success(response,"500")

    @patch('apps.home.models.NetworthBackup.objects.filter')
    def test_restore_backup_exception_db(self,mock_filter,user,client):
        # mock method must return exception
        mock_filter.return_value = Exception("Simulated DB error")
        user = User.objects.create_user("sam@mail.com","sam@mail.com","Test@123")
        up_actions.do_create_user_profile(user,country="IN")
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)

        networth_name=generate_random_text(10)
        category_name1=generate_random_text(10)
        category_name2=generate_random_text(10)
        ag_name1=generate_random_text(10)
        ag_name2=generate_random_text(10)
        i1_name=generate_random_text(10)
        i2_name=generate_random_text(10)
        i3_name=generate_random_text(10)
        i4_name=generate_random_text(10)
        i5_name=generate_random_text(10)
        i6_name=generate_random_text(10)


        backup_object = self.create_test_data_for_advanced_for_user(user,networth_name,category_name1,category_name2,ag_name1,ag_name2,i1_name,i2_name,i3_name,i4_name,i5_name,i6_name)
        # make a get request to the restore backup page
        response = client.get(reverse("restore_backup", args=[backup_object.id]))
        time.sleep(self.AVG_WAIT_TIME)
        assert response.status_code == 200
        #assert 'form' in response.context
        assert response.context['msg'] == "There was an error during restore operation, please contact support to get issue resolved."
        assert 'home/restore-backup.html' in [t.name for t in response.templates]

    def test_restore_backup_view_invalid(self,client):
        user = User.objects.create_user("sam@mail.com","sam@mail.com","Test@123")
        up_actions.do_create_user_profile(user,country="IN")
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)

        # make a get request to the restore backup page
        response = client.get(reverse("restore_backup", args=[2801281928120]))
        # Check that the response status code is 404
        assert response.status_code == 200
        assert response.context["msg"] == "There was an error during restore operation, please contact support to get issue resolved." 
        validate_response(response,200,b'InvestODiary -  Restore Backup','home/restore-backup.html')

    def test_restore_backup_view(self,client):
        user = User.objects.create_user("sam@mail.com","sam@mail.com","Test@123")
        up_actions.do_create_user_profile(user,country="IN")
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)

        networth_name=generate_random_text(10)
        category_name1=generate_random_text(10)
        category_name2=generate_random_text(10)
        ag_name1=generate_random_text(10)
        ag_name2=generate_random_text(10)
        i1_name=generate_random_text(10)
        i2_name=generate_random_text(10)
        i3_name=generate_random_text(10)
        i4_name=generate_random_text(10)
        i5_name=generate_random_text(10)
        i6_name=generate_random_text(10)


        backup_object = self.create_test_data_for_advanced_for_user(user,networth_name,category_name1,category_name2,ag_name1,ag_name2,i1_name,i2_name,i3_name,i4_name,i5_name,i6_name)

        # make a get request to the restore backup page
        response = client.get(reverse("restore_backup", args=[backup_object.id]))
        time.sleep(self.AVG_WAIT_TIME)
        # Check that the response status code is 200
        assert response.status_code == 200
        assert response.context["msg"] == "Restoring backup completed successfully"
        
        # validate request response
        validate_response(response,200,b'InvestODiary -  Restore Backup','home/restore-backup.html')

        # get networth from networth table for user
        networth = Networth.objects.get(user=user,is_active=True)
        assert networth.name == networth_name
        assert networth.amount == 32
        assert networth.is_active == True

        # get baseunits from baseunits table for networth
        baseunit = BaseUnit.objects.get(networth=networth)
        assert baseunit.name == "Lakhs"
        assert baseunit.value == 100000
        assert baseunit.networth == networth

        # get categories for networth from category table
        categories = Category.objects.filter(networth=networth)
        assert len(categories) == 2
        
        # validate categories are restored correctly

        # validate category1 restored correctly
        category1 = Category.objects.get(name=category_name1,networth=networth)
        assert category1.weightage == 50
        assert category1.display_amount_in_base_unit==False
        assert category1.is_active == True  
        # validate ag1 restored correctly
        ag1 = AssetGroup.objects.get(name=ag_name1,category=category1)
        assert ag1.weightage == 50
        assert ag1.is_active == True
        assert ag1.display_amount_in_base_unit==False
        # fetch all instruments for ag1
        instruments = Instrument.objects.filter(asset=ag1)
        # validate each instrument is restored correctly
        for instrument in instruments:
            if instrument.name==i1_name:
                assert instrument.weightage == 10
                assert instrument.amount_invested == 10000
                assert instrument.current_value == 12000
                assert instrument.is_active == True
                assert instrument.display_amount_in_base_unit==True
            elif instrument.name==i2_name:
                assert instrument.weightage == 10
                assert instrument.amount_invested == 10000
                assert instrument.current_value == 13000
                assert instrument.is_active == True
                assert instrument.display_amount_in_base_unit==True
            elif instrument.name==i3_name:
                assert instrument.weightage == 10
                assert instrument.amount_invested == 10000
                assert instrument.current_value == 7000
                assert instrument.is_active == True
                assert instrument.display_amount_in_base_unit==True

        # validate category2 restored correctly
        category2 = Category.objects.get(name=category_name2,networth=networth)
        assert category2.weightage == 50
        assert category2.display_amount_in_base_unit==False
        assert category2.is_active == True
        # validate ag2 restored correctly
        ag2 = AssetGroup.objects.get(name=ag_name2,category=category2)
        assert ag2.name == ag_name2
        assert ag2.weightage == 50
        assert ag2.is_active == True
        assert ag2.display_amount_in_base_unit==False
        # fetch all instruments for ag2
        instruments = Instrument.objects.filter(asset=ag2)
        # validate each instrument is restored correctly
        for instrument in instruments:
            if instrument.name==i4_name:
                assert instrument.weightage == 10
                assert instrument.amount_invested == 10000
                assert instrument.current_value == 12000
                assert instrument.is_active == True
                assert instrument.display_amount_in_base_unit==True
            elif instrument.name==i5_name:
                assert instrument.weightage == 10
                assert instrument.amount_invested == 10000
                assert instrument.current_value == 13000
                assert instrument.is_active == True
                assert instrument.display_amount_in_base_unit==True
            elif instrument.name==i6_name:
                assert instrument.weightage == 10
                assert instrument.amount_invested == 10000
                assert instrument.current_value == 7000
                assert instrument.is_active == True
                assert instrument.display_amount_in_base_unit==True






################################################################################################################################
# Delete Backup Tests
################################################################################################################################
    def test_backups_delete_raise_exception(self,user,client,mocker):
        mocker.patch.object(backups_lib, 'fetch_post_response_delete', side_effect=Exception("Simulated error"))
        new_user = User.objects.create_user("sam@mail.com","sam@mail.com","Test@123")
        create_test_data_for_user(new_user)
        backup_name = generate_random_text(10)
        backup_actions.do_create_backup(new_user,backup_name)
        self.initialize_user(new_user,False,False,True)
        self.user_login(client,new_user)

        backup = Backup.objects.get(name=backup_name)
        assert backup.status=="Completed"
        # Make a GET request to the edit backup page
        response = client.get(reverse("delete_backup", args=[backup.id]))
        assert_response_success(response,"500")

    def test_delete_backup_view(self,client):
        new_user = User.objects.create_user("sam@mail.com","sam@mail.com","Test@123")
        create_test_data_for_user(new_user)
        backup_name = generate_random_text(10)
        backup_actions.do_create_backup(new_user,backup_name)
        self.initialize_user(new_user,False,False,True)
        self.user_login(client,new_user)

        backup = Backup.objects.get(name=backup_name)
        assert backup.status=="Completed"
        # Make a GET request to the edit backup page
        response = client.get(reverse("delete_backup", args=[backup.id]))
        time.sleep(self.AVG_WAIT_TIME)  
        # Check that the response status code is 302
        assert response.status_code == 302
        
        # check that the backup is deleted
        assert Backup.objects.filter(id=backup.id)[0].status=="Deleted"


################################################################################################################################
# Edit Backup Tests
################################################################################################################################
    def test_edit_backup_view(self,client):
        new_user = User.objects.create_user("sam@mail.com","sam@mail.com","Test@123")
        create_test_data_for_user(new_user)
        backup_name = generate_random_text(10)
        backup_actions.do_create_backup(new_user,backup_name)
        self.initialize_user(new_user,False,False,True)
        self.user_login(client,new_user)

        backup = Backup.objects.get(name=backup_name)

        # Make a GET request to the edit backup page
        response = client.get(reverse("edit_backup", args=[backup.id]))

        # Check that the response status code is 200
        assert response.status_code == 200
        
        # create data for backup form
        updated_name = "Updated Backup Name"
        data = backup_testdata.set_default_backup_data(updated_name)

        # call post_response_using_params
        response = post_response_using_params(client,'edit_backup',data,param_set=[backup.id])

        # check response status code
        assert response.status_code == 302
        
        # check that the backup was updated
        backup=Backup.objects.get(id=backup.id)
        backup.refresh_from_db()
        backup_testdata.assert_backup(backup,new_user,updated_name)
    
    def test_backups_edit_raise_exception(self,user,client,mocker):
        mocker.patch.object(backups_lib, 'fetch_get_response_edit', side_effect=Exception("Simulated error"))
        new_user = User.objects.create_user("sam@mail.com","sam@mail.com","Test@123")
        create_test_data_for_user(new_user)
        backup_name = generate_random_text(10)
        backup_actions.do_create_backup(new_user,backup_name)
        self.initialize_user(new_user,False,False,True)
        self.user_login(client,new_user)

        backup = Backup.objects.get(name=backup_name)

        # make a get request to edit back up page
        response = client.get(reverse("edit_backup", args=[backup.id]))
        assert_response_success(response,"500")

    def test_edit_backup_invalid_data(self, client):
        new_user = User.objects.create_user("sam@mail.com","sam@mail.com","Test@123")
        create_test_data_for_user(new_user)
        backup_name = generate_random_text(10)
        backup_actions.do_create_backup(new_user,backup_name)
        self.initialize_user(new_user,False,False,True)
        self.user_login(client,new_user)

        backup = Backup.objects.get(name=backup_name)

        # make a get request to edit back up page
        response = client.get(reverse("edit_backup", args=[backup.id]))

        # check response status code
        assert response.status_code == 200

        # create data for backup form
        updated_name = generate_invalid_text()
        data = backup_testdata.set_default_backup_data(updated_name)
        response = post_response_using_params(client,"edit_backup",data,param_set=[backup.id])

        # validate the response
        validate_response(response,200,b'InvestODiary -  Backups Summary','home/backups.html')

        # asserrt that the error displayed on the page
        assert "form" in response.context
        form_errors = response.context["form"].errors
        assert form_errors["name"][0] == "Backup Name must contain only letters, numbers, underscores or hyphens."
        


################################################################################################################################
# Create Backup Tests
################################################################################################################################
    def test_get_create_backups_existing_backup_simple(self,client):
        """
        Test create backups view for an authenticated user
        """
        new_user = User.objects.create_user("sam@mail.com","sam@mail.com","Test@123")
        create_test_data_for_user(new_user)
        backup_name = generate_random_text(10)
        backup_actions.do_create_backup(new_user,backup_name)
        self.initialize_user(new_user,False,False,True)
        self.user_login(client,new_user)

        response = get_response_using_view_name(client,"create_backup")
        assert_response_success(response,'create_backup')
        assert_data_in_context(response,['form'])
        backup = backup_actions.get_backup_by_name(new_user,backup_name)
        assert backup is not None
        assert backup.status == "Completed"
        

    
    def test_post_create_backups_existing_backup_simple(self,client):
        """
        Test create backups view for an authenticated user
        """
        
        new_user = User.objects.create_user("sam@mail.com","sam@mail.com","Test@123")
        create_test_data_for_user(new_user)
        self.initialize_user(new_user,False,False,True)
        self.user_login(client,new_user)

        backup_name = generate_random_text(10)
        data = backup_testdata.set_default_backup_data(backup_name)
        response = post_response_using_view_name(client,"create_backup",data,new_user)
        # Check that the response status code is a redirect (302)
        assert response.status_code == 302
        backup = backup_actions.get_backup_by_name(new_user,backup_name)
        assert backup is not None
        assert backup.status == "Completed"
        

    def test_post_create_backups_ineligible_data(self,client):
        """
        Test create backups view when there is no data to backup or user did not create any app data
        """
        
        Networth.objects.filter(user__email="sam@mail.com").delete()
        User.objects.filter(email="sam@mail.com").delete()
        new_user = User.objects.create_user("sam@mail.com","sam@mail.com","Test@123")
        userprofile_actions.do_create_user_profile(new_user,country="IN")
        self.initialize_user(new_user,False,False,True)
        self.user_login(client,new_user)
        backup_name = generate_random_text(10)
        data = backup_testdata.set_default_backup_data(backup_name)
        
        networth = networth_actions.do_create_networth("Test Networth",32,new_user)
        baseunit = baseunit_actions.do_create_baseunit_with_user(new_user,networth)
        category1 = category_actions.do_create_category("Test Cat1",50,new_user)
        ag1 = ag_actions.do_create_assetgroup("Test AG1",50,category1,acting_user=new_user)

        response = post_response_using_view_name(client,"create_backup",data,new_user)

        assert response.status_code == 200
        assert 'form' in response.context
        assert "Backup can't be created, there is no data to backup. You need to have atleast one valid instrument as part of your portfolio. Please add some instruments and try again." in response.context["error_message"]

    def test_post_create_backups_invalid_form(self,client):
        """
        Test create backups view for an authenticated user
        """
        
        new_user = User.objects.create_user("sam@mail.com","sam@mail.com","Test@123")
        create_test_data_for_user(new_user)
        self.initialize_user(new_user,False,False,True)
        self.user_login(client,new_user)

        backup_name = generate_invalid_text()
        data = backup_testdata.set_default_backup_data(backup_name)
        response = post_response_using_view_name(client,"create_backup",data,new_user)
        assert response.status_code == 200
        assert 'form' in response.context
        form_errors = response.context["form"].errors
        assert form_errors["name"][0] == "Backup Name must contain only letters, numbers, underscores or hyphens."
        qs = backup_actions.get_backups(new_user)
        assert len(qs) == 0


################################################################################################################################
# View Backup Tests
################################################################################################################################
    def test_backups_view_raise_exception(self,user,client,mocker):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        mocker.patch.object(backups_lib, 'fetch_get_response_view', side_effect=Exception("Simulated error"))
        response = get_response_using_view_name(client,"view_backups")
        assert_response_success(response,"500")

    def test_backups_view_existing_backup(self,client):
        """
        Test backups view for an authenticated user
        """
        new_user = User.objects.create_user("sam@mail.com","sam@mail.com","Test@123")
        create_test_data_for_user(new_user)
        backup_actions.do_create_backup(new_user,"sasjalskja")
        self.initialize_user(new_user,False,False,True)
        self.user_login(client,new_user)
        response = get_response_using_view_name(client,"view_backups")
        assert_response_success(response,'view_backups')
        assert_data_in_context(response,['backup_list'])
    
    def test_backups_view_no_backup(self,user,client):
        """
        Test backups view for an authenticated user
        """
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        
        response = get_response_using_view_name(client,"view_backups")
        assert_response_success(response,'view_backups')
        assert_data_not_in_context(response,['backup_list'])
    
    def test_backups_view_backup_complete(self,client):
        user = User.objects.create_user("sam@mail.com","sam@mail.com","Test@123")
        up_actions.do_create_user_profile(user,country="IN")
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)

        networth = networth_actions.do_create_networth("Test Networth",32,user)
        baseunit = baseunit_actions.do_create_baseunit_with_user(user,networth)
        category1 = category_actions.do_create_category("Test Cat1",50,user)
        ag1 = ag_actions.do_create_assetgroup("Test AG1",50,category1,acting_user=user)
        i1 = instuments_actions.do_create_instrument(name="sashjkas",weightage=10,amount_invested=10000,asset=ag1, acting_user=user,current_value=12000)
        i2 = instuments_actions.do_create_instrument(name="hdkahsdk",weightage=10,amount_invested=10000,asset=ag1, acting_user=user,current_value=13000)
        i3 = instuments_actions.do_create_instrument(name="sasiaosi",weightage=10,amount_invested=10000,asset=ag1, acting_user=user,current_value=7000)

        category2 = category_actions.do_create_category("Test Cat2",50,user)
        ag2 = ag_actions.do_create_assetgroup("Test AG2",50,category2,acting_user=user)
        i4 = instuments_actions.do_create_instrument(name="eryiewryie",weightage=10,amount_invested=10000,asset=ag2, acting_user=user,current_value=12000)
        i5 = instuments_actions.do_create_instrument(name="wuqoiwqow",weightage=10,amount_invested=10000,asset=ag2, acting_user=user,current_value=13000)
        i6 = instuments_actions.do_create_instrument(name="cnmzxbcnmzb",weightage=10,amount_invested=10000,asset=ag2, acting_user=user,current_value=7000)

        backup_name = generate_random_text(10)
        backup_actions.do_create_backup(user,backup_name)

        backups = backup_actions.get_backups(user)

        for backup in backups:
            assert backup.name == backup_name
            assert backup.status == "Completed"
            assert backup.user == user
        
        backup_object = backup_actions.get_backup_by_name(user,backup_name)

        networth_bkup_data = NetworthBackup.objects.get(user=user.id,backup=backup_object)
        assert networth_bkup_data.name == "Test Networth"
        assert networth_bkup_data.amount == 32
        assert networth_bkup_data.is_active == True

        networth_bkup_id = networth_bkup_data.src_networth_id

        baseunit_bkup_data = BaseUnitBackup.objects.get(backup=backup_object)
        assert baseunit_bkup_data.name == "Lakhs"
        assert baseunit_bkup_data.value == 100000
        assert baseunit_bkup_data.networth == networth_bkup_id

        categories_bkup_data = CategoryBackup.objects.filter(backup=backup_object)
        assert len(categories_bkup_data) == 2
        # validate all categories are stored in backup
        for category_bkup_data in categories_bkup_data:
            # validate category1 data is stored correctly
            if category_bkup_data.src_category_id == category1.id:
                assert category_bkup_data.name == "Test Cat1"
                assert category_bkup_data.weightage == 50
                assert category_bkup_data.networth == networth_bkup_id
                assert category_bkup_data.display_amount_in_base_unit == category1.display_amount_in_base_unit
                assert category_bkup_data.is_active == True
                # fetch all asset groups of category1 from asset group backup
                ags_bkup_data = AssetGroupBackup.objects.filter(category=category_bkup_data.src_category_id,backup=backup_object)
                assert len(ags_bkup_data) == 1
                # validate all asset groups are backed up correctly
                for ag_bkup_data in ags_bkup_data:
                    assert ag_bkup_data.src_asset_id == ag1.id
                    assert ag_bkup_data.name == "Test AG1"
                    assert ag_bkup_data.weightage == 50
                    assert ag_bkup_data.category == category1.id
                    assert ag_bkup_data.display_amount_in_base_unit == ag1.display_amount_in_base_unit
                    assert ag_bkup_data.is_active == True
                    # fetch all instruments of asset group1 from instrument backup
                    insts_bkup_data = InstrumentBackup.objects.filter(asset=ag_bkup_data.src_asset_id,backup=backup_object)
                    
                    assert len(insts_bkup_data) == 3
                    
                    # validate first instrument is backed up correctly
                    assert insts_bkup_data[0].src_instrument_id == i1.id
                    assert insts_bkup_data[0].name == "sashjkas"
                    assert insts_bkup_data[0].weightage == 10
                    assert insts_bkup_data[0].amount_invested == 10000
                    assert insts_bkup_data[0].current_value == 12000
                    assert insts_bkup_data[0].asset == ag1.id
                    assert insts_bkup_data[0].display_amount_in_base_unit == i1.display_amount_in_base_unit
                    assert insts_bkup_data[0].is_active == True

                    # validate second instrument is backed up correctly
                    assert insts_bkup_data[1].src_instrument_id == i2.id
                    assert insts_bkup_data[1].name == "hdkahsdk"
                    assert insts_bkup_data[1].weightage == 10
                    assert insts_bkup_data[1].amount_invested == 10000
                    assert insts_bkup_data[1].current_value == 13000
                    assert insts_bkup_data[1].asset == ag1.id
                    assert insts_bkup_data[1].display_amount_in_base_unit == i2.display_amount_in_base_unit
                    assert insts_bkup_data[1].is_active == True

                    # validate third instrument is backed up correctly
                    assert insts_bkup_data[2].src_instrument_id == i3.id
                    assert insts_bkup_data[2].name == "sasiaosi"
                    assert insts_bkup_data[2].weightage == 10
                    assert insts_bkup_data[2].amount_invested == 10000
                    assert insts_bkup_data[2].current_value == 7000
                    assert insts_bkup_data[2].asset == ag1.id
                    assert insts_bkup_data[2].display_amount_in_base_unit == i3.display_amount_in_base_unit
                    assert insts_bkup_data[2].is_active == True
                        
            else:
                assert category_bkup_data.name == "Test Cat2"
                assert category_bkup_data.weightage == 50
                assert category_bkup_data.networth == networth_bkup_id
                assert category_bkup_data.display_amount_in_base_unit == category1.display_amount_in_base_unit
                assert category_bkup_data.is_active == True
                ags_bkup_data = AssetGroupBackup.objects.filter(category=category_bkup_data.src_category_id,backup=backup_object)
                assert len(ags_bkup_data) == 1
                # validate all asset groups are backed up correctly
                for ag_bkup_data in ags_bkup_data:
                    assert ag_bkup_data.src_asset_id == ag2.id
                    assert ag_bkup_data.name == "Test AG2"
                    assert ag_bkup_data.weightage == 50
                    assert ag_bkup_data.category == category2.id
                    assert ag_bkup_data.display_amount_in_base_unit == ag2.display_amount_in_base_unit
                    assert ag_bkup_data.is_active == True
                    # fetch all instruments of asset group1 from instrument backup
                    insts_bkup_data = InstrumentBackup.objects.filter(asset=ag_bkup_data.src_asset_id,backup=backup_object)
                    
                    assert len(insts_bkup_data) == 3
                    
                    # validate first instrument is backed up correctly
                    assert insts_bkup_data[0].src_instrument_id == i4.id
                    assert insts_bkup_data[0].name == "eryiewryie"
                    assert insts_bkup_data[0].weightage == 10
                    assert insts_bkup_data[0].amount_invested == 10000
                    assert insts_bkup_data[0].current_value == 12000
                    assert insts_bkup_data[0].asset == ag2.id
                    assert insts_bkup_data[0].display_amount_in_base_unit == i1.display_amount_in_base_unit
                    assert insts_bkup_data[0].is_active == True

                    # validate second instrument is backed up correctly
                    assert insts_bkup_data[1].src_instrument_id == i5.id
                    assert insts_bkup_data[1].name == "wuqoiwqow"
                    assert insts_bkup_data[1].weightage == 10
                    assert insts_bkup_data[1].amount_invested == 10000
                    assert insts_bkup_data[1].current_value == 13000
                    assert insts_bkup_data[1].asset == ag2.id
                    assert insts_bkup_data[1].display_amount_in_base_unit == i2.display_amount_in_base_unit
                    assert insts_bkup_data[1].is_active == True

                    # validate third instrument is backed up correctly
                    assert insts_bkup_data[2].src_instrument_id == i6.id
                    assert insts_bkup_data[2].name == "cnmzxbcnmzb"
                    assert insts_bkup_data[2].weightage == 10
                    assert insts_bkup_data[2].amount_invested == 10000
                    assert insts_bkup_data[2].current_value == 7000
                    assert insts_bkup_data[2].asset == ag2.id
                    assert insts_bkup_data[2].display_amount_in_base_unit == i3.display_amount_in_base_unit
                    assert insts_bkup_data[2].is_active == True

                



