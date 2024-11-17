
from apps.home.models import(
    BaseUnit,
    Networth
    )
from django.contrib.auth.models import User
from typing import Optional
from django.utils.translation import gettext as _
from django.db import transaction
from apps.home.lib.exceptions import JsonableError
from apps.home.actions import baseunit as baseunit_actions
from apps.home.lib import constants

def update_model_fields(instance: Networth, update_data):
    # Iterate through the dictionary of update data
    for field, value in update_data.items():
        # Update the model instance's field with the provided value using setattr
        setattr(instance, field, value)
    
    # Save the instance to commit the changes to the database
    instance.save()
    
    # Return the updated instance
    return instance

def get_networth(user):
      return Networth.objects.get(user=user, is_active=True)

def do_create_networth(name:str,amount:int, user:User)-> Networth:
    with transaction.atomic():
            networth = Networth.objects.create(
                name=name,
                amount=amount,
                user=user,
                is_active = True
            )
            #baseunit_actions.do_create_baseunit(constants.DEFAULT_BASE_UNIT_NAME,constants.DEFAULT_BASE_UNIT_VALUE,networth)
            baseunit_actions.do_create_baseunit_with_user(user,networth)
    return networth
    
