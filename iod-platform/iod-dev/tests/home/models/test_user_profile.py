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
    UserProfile
)
from django.core.exceptions import ObjectDoesNotExist,ValidationError
from apps.home.lib.exceptions import JsonableError
from apps.home.actions import instruments, networth as networth_actions

################################################################################################################################
# Category
################################################################################################################################


@pytest.mark.django_db
class Test_UserProfile_Models(BaseTest):

    def test_first_name_max_length(self,user):        
        profile = UserProfile.objects.get(user=user)
        max_length = profile._meta.get_field('first_name').max_length
        assert max_length == 120

    def test_last_name_max_length(self,user):
        profile = UserProfile.objects.get(user=user)
        max_length = profile._meta.get_field('last_name').max_length
        assert max_length == 120

    def test_address_max_length(self,user):
        profile = UserProfile.objects.get(user=user)
        max_length = profile._meta.get_field('address').max_length
        assert max_length == 120

    def test_bio_max_length(self,user):
        profile = UserProfile.objects.get(user=user)
        max_length = profile._meta.get_field('bio').max_length
        assert max_length == 500

    def test_user_foreign_key(self,user):
        profile = UserProfile.objects.get(user=user)
        user = User.objects.get(username=user.username)
        assert profile.user == user
       