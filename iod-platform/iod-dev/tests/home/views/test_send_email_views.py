from django.core import mail
import pytest
from tests.test_classes import BaseTest
from django.urls import reverse
from test_common import (
    delete_response_using_params,
    get_response_using_view_name,
    assert_response_success,
    assert_data_in_context,
    post_response_using_params
)
from tests.common.test_data.user_profile import (
    set_default_userprofile_data
)
from tests.common.test_data import nominee as nominee_testdata
from test_common import (
    get_response_using_view_name,
    post_response_using_view_name,
    validate_response,
    assert_response_redirect,
    assert_response_success
)
from apps.home.models import(
    AssetGroup,
    BaseUnit,
    Category,
    Instrument,
    UserNominee,
    UserProfile
)
from django.contrib.auth.models import User
from unittest.mock import patch
from apps.home.lib import(
    email as email_lib
)
@pytest.mark.django_db
class Test_SendNomineeMail_Views(BaseTest):
    def test_send_nominee_email_with_currentvalue(self,client,user,nominee,networth,category,assetgroup):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)

        category = Category.objects.get(id=category.id)
        category.weightage = 100
        category.save()

        assetgroup = AssetGroup.objects.get(id=assetgroup.id)
        assetgroup.weightage = 100
        assetgroup.save()

        unit = BaseUnit.objects.get(networth=networth)
        unit.value = 100000
        unit.save()
        
        # # Create some test data
        i1 = Instrument.objects.create(name='Test AG 1', amount_invested=1000000,current_value = 1200000, asset=assetgroup)
        i2 = Instrument.objects.create(name='Test Ag 2', amount_invested=2000000,current_value=2800000, asset=assetgroup)
        
        # Call the send_email view
        response = client.get(reverse('send_nominee_email'))

        # Check that one message has been sent
        assert len(mail.outbox) == 1

        # Verify the subject of the first message
        assert mail.outbox[0].subject == 'Networth Summary Update'

    def test_send_nominee_email_without_currentvalue(self,client,user,nominee,networth,category,assetgroup):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)

        category = Category.objects.get(id=category.id)
        category.weightage = 100
        category.save()

        assetgroup = AssetGroup.objects.get(id=assetgroup.id)
        assetgroup.weightage = 100
        assetgroup.save()

        unit = BaseUnit.objects.get(networth=networth)
        unit.value = 100000
        unit.save()

        # # Create some test data
        i1 = Instrument.objects.create(name='Test AG 1', amount_invested=1000000,current_value = 0, asset=assetgroup)
        i2 = Instrument.objects.create(name='Test Ag 2', amount_invested=2000000,current_value=0, asset=assetgroup)

        # Call the send_email view
        response = client.get(reverse('send_nominee_email'))

        # Check that one message has been sent
        assert len(mail.outbox) == 1

        # Verify the subject of the first message
        assert mail.outbox[0].subject == 'Networth Summary Update'

    def test_send_nominee_email_without_nominee(self,client,user,networth,category,assetgroup):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)

        category = Category.objects.get(id=category.id)
        category.weightage = 100
        category.save()

        assetgroup = AssetGroup.objects.get(id=assetgroup.id)
        assetgroup.weightage = 100
        assetgroup.save()

        unit = BaseUnit.objects.get(networth=networth)
        unit.value = 100000
        unit.save()

        # # Create some test data
        i1 = Instrument.objects.create(name='Test AG 1', amount_invested=1000000,current_value = 0, asset=assetgroup)
        i2 = Instrument.objects.create(name='Test Ag 2', amount_invested=2000000,current_value=0, asset=assetgroup)

        # Call the send_email view
        response = client.get(reverse('send_nominee_email'))

        # Check that one message has been sent
        assert len(mail.outbox) == 0
    
    
    def test_send_nominee_email_with_invalid_raise_exception(self,client,user,nominee,networth,category,assetgroup,mocker):
        mocker.patch.object(email_lib, 'fetch_post_response_send', side_effect=Exception("Simulated error"))
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        
        response = client.get(reverse('send_nominee_email'))

        # Assert that the response is an error (status code 500)
        assert_response_success(response, "500")

    def test_send_nominee_email_with_invalid_nominee_data(self,client,user,nominee,networth,category,assetgroup):
        with patch('django.core.mail.send_mail') as mock_send_mail:
            mock_send_mail.side_effect = Exception()
        
            self.initialize_user(user,False,False,True)
            self.user_login(client,user)
            response = client.get(reverse('send_nominee_email'))
            assert_response_redirect(response,'view_nominee')
            validate_response(response,302,b'','home/email.html')
       