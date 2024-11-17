import pytest
from tests.test_classes import BaseTest
from django.contrib.auth.models import User
from apps.home.actions import instruments, networth, category, assetgroup
from apps.home.models import (
    BaseUnit,
    Networth,
    Category,
    AssetGroup,
    Instrument,
    UserProfile,
    UserNominee
)
from django.core.exceptions import ObjectDoesNotExist,ValidationError
from apps.home.lib.exceptions import JsonableError
from apps.home.actions import instruments, networth as networth_actions

################################################################################################################################
# Nominee
################################################################################################################################


@pytest.mark.django_db
class Test_Nominee_Models(BaseTest):
    def test_first_name_max_length(self,user):        
        profile = UserProfile.objects.get(user=user)
        max_length = profile._meta.get_field('first_name').max_length
        assert max_length == 120
    
    def test_name_label(self,user,nominee):
        field_label = nominee._meta.get_field('name').verbose_name
        assert field_label == 'name'
    
    def test_email_label(self,user,nominee):
        field_label = nominee._meta.get_field('email').verbose_name
        assert field_label == 'email'

    def test_status_label(self,user,nominee):
        assert nominee.status == 'A'
    
    def test_object_name_is_name(self,user,nominee):
        expected_object_name = f'{nominee.name}'
        assert expected_object_name == str(nominee)
    