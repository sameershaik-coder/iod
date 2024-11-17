from apps.home.models import(
    BaseUnit,
    Networth,
    Category,
    AssetGroup
    )
from django.contrib.auth.models import User
from django.db import transaction
from apps.home.lib.exceptions import JsonableError
from django.db.models import Sum
from django.utils.translation import gettext as _


def get_assets_with_order(category:Category, order_by='-weightage'):
    return AssetGroup.objects.filter(category = category).order_by(order_by)

def get_asset_group(id:int, user)->AssetGroup:
    return AssetGroup.objects.get(id=id, category__networth__user=user)

def check_asset_group_exists_by_name(name:str, category:Category)->bool:
    return AssetGroup.objects.filter(name=name,category=category).exists()

def do_delete_asset(asset:AssetGroup, _cascade: bool = True, *, acting_user: User)->None:
    networth_user = asset.category.networth.user
    if networth_user == acting_user:
        with transaction.atomic():
            asset.delete()
    else:
        raise JsonableError(_("User does not have permissions to this asset group and category"))
        

def do_create_assetgroup(name:str,weightage:int,category:Category, acting_user:User)-> AssetGroup:
    result = None
    qs = AssetGroup.objects.filter(name=name,category=category)
    if qs.count() == 0:
        networth_user = category.networth.user 
        if networth_user == acting_user:
            existing_assets_weightage_sum = get_assets_weightage_sum(category)
            new_assets_weightage_sum = existing_assets_weightage_sum + weightage
            if new_assets_weightage_sum <= 100 :
                with transaction.atomic():
                    result = AssetGroup.objects.create(
                        name=name,
                        weightage=weightage,
                        category=category
                    )
            else:
                remaining_weightage = 100 - existing_assets_weightage_sum
                raise JsonableError(_(f"Asset Group weightage cannot exceed {remaining_weightage}%."))
        else:
            raise JsonableError(_("User does not have permissions to this asset group and category"))
    else:
        raise JsonableError(_("Asset Group already exists for given name and category combination"))
    return result

def get_assets_weightage_sum(category : Category):
    existing_assets_weightage_sum = 0
    existing_assets = AssetGroup.objects.filter(category = category)
    if existing_assets.count() > 0:
        existing_assets_weightage_sum = existing_assets.aggregate(Sum('weightage')).get("weightage__sum")  
    return  existing_assets_weightage_sum