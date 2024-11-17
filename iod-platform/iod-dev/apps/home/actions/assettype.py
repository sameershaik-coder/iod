from apps.home.models import(
    BaseUnit,
    Networth
    )
from apps.configuration.models import AssetType
from django.contrib.auth.models import User
from typing import Optional
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from apps.home.lib.exceptions import JsonableError
from django.utils.translation import gettext as _

def do_create_assettype(name:str,weightage:int,user:User)-> AssetType:
    assettype = None
    with transaction.atomic():
        networth = Networth.objects.get(user=user, is_active=True)
        assettype = AssetType.objects.create(
            name = name,
            weightage = weightage,
            networth = networth
        )
        assettype.save()
        
    return assettype
