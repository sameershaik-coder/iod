from apps.home.models import(
    BaseUnit,
    Networth,
    Category
    )
from django.contrib.auth.models import User
from typing import Optional
from django.db import transaction
from apps.home.lib.exceptions import JsonableError
from django.db.models import Sum
from django.utils.translation import gettext as _

def get_categories_with_order(networth:Networth, order_by='-weightage'):
    return Category.objects.filter(networth = networth).order_by(order_by)

def check_category_exists_with_name(name:str,networth:Networth):
    qs = Category.objects.filter(name=name,networth=networth)
    if qs.count() > 0:
        return True
    else:
        return False
    

def do_create_category_with_message(name:str,weightage:int,user:User):
    category = None
    networth = Networth.objects.get(user=user, is_active=True)
    qs = Category.objects.filter(name=name,networth=networth)
    error_message = None
    if qs.count() == 0:
        networth_user = networth.user 
        if networth_user == user:
            existing_categories_weightage_sum = get_categories_weightage_sum(networth)
            new_cat_weightage_sum = existing_categories_weightage_sum + weightage
            if new_cat_weightage_sum <= 100 :
                with transaction.atomic():
                    category = Category.objects.create(
                        name = name,
                        weightage = weightage,
                        networth = networth
                    )
                    category.save()
            else:
                remaining_weightage = new_cat_weightage_sum - 100
                error_message = _(f"category weightage cannot exceed {remaining_weightage}%.")
    else:
        error_message = _("Category with same name already exist for this networth")
    return category, error_message

def get_category(category_id: int, user: User) -> Category:
    networth = Networth.objects.get(user=user, is_active=True)
    return Category.objects.get(id=category_id, networth=networth)

def get_categories_by_networth(networth,user):
    return Category.objects.filter(networth=networth,networth__user=user).order_by('-weightage')

def do_delete_category(category:Category, _cascade: bool = True, *, acting_user: User)->None:
    result = False
    networth_user = category.networth.user
    if networth_user == acting_user:
        with transaction.atomic():
            category.delete()
            result = True
    else:
        raise JsonableError(_("User does not have permissions to this category and network"))
    return result

def do_create_category(name:str,weightage:int,user:User)-> Category:
    category = None
    networth = Networth.objects.get(user=user, is_active=True)
    qs = Category.objects.filter(name=name,networth=networth)
    if qs.count() == 0:
        networth_user = networth.user 
        if networth_user == user:
            existing_categories_weightage_sum = get_categories_weightage_sum(networth)
            new_cat_weightage_sum = existing_categories_weightage_sum + weightage
            if new_cat_weightage_sum <= 100 :
                with transaction.atomic():
                    category = Category.objects.create(
                        name = name,
                        weightage = weightage,
                        networth = networth
                    )
                    category.save()
            else:
                remaining_weightage = new_cat_weightage_sum - 100
                raise JsonableError(_(f"category weightage cannot exceed {remaining_weightage}%."))
    else:
        raise JsonableError(_("Category with same name already exist for this networth"))
    return category


def get_categories_weightage_sum(networth : Networth):
    existing_cat_weightage_sum = 0
    existing_categories = Category.objects.filter(networth = networth)
    if existing_categories.count() > 0:
        existing_cat_weightage_sum = existing_categories.aggregate(Sum('weightage')).get("weightage__sum")  
    return  existing_cat_weightage_sum