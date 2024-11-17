
from apps.home.models import(
    AssetGroup,
    Instrument
)
from django.contrib.auth.models import User
from typing import Optional
from django.db.models import Sum
from django.utils.translation import gettext as _
from django.db import transaction
from apps.home.lib.exceptions import JsonableError


def update_model_fields(instance: Instrument, update_data):
    # Iterate through the dictionary of update data
    for field, value in update_data.items():
        # Update the model instance's field with the provided value using setattr
        setattr(instance, field, value)
    
    # Save the instance to commit the changes to the database
    instance.save()
    
    # Return the updated instance
    return instance

def check_instrument_exists(name:str,asset:AssetGroup)->bool:
    return Instrument.objects.filter(name=name,asset=asset).count() > 0

def get_instrument_by_id(id:int, user:User)->Instrument:
    return Instrument.objects.get(id=id, asset__category__networth__user=user)

def get_instruments_by_asset(asset:AssetGroup, order_by='-amount_invested'):
    return (Instrument.objects.filter(asset = asset)).order_by(order_by)

def do_delete_instrument(instrument:Instrument, _cascade: bool = True, *, acting_user: Optional[User])->None:
    networth_user = instrument.asset.category.networth.user
    if networth_user == acting_user:
        with transaction.atomic():
            instrument.delete()
    else:
        raise JsonableError(_("User does not have permissions to this asset group and category"))

def do_create_instrument(name:str,weightage:int,amount_invested:int,asset:AssetGroup, acting_user:User,current_value=0)-> Instrument:
    result = None
    qs = Instrument.objects.filter(name=name,asset=asset)
    if qs.count() == 0:
        networth_user = asset.category.networth.user
        if networth_user == acting_user:
            existing_instruments_weightage_sum = get_instruments_weightage_sum(asset)
            new_instruments_weightage_sum = existing_instruments_weightage_sum + weightage
            if new_instruments_weightage_sum <= 100 :
                with transaction.atomic():
                    result =  Instrument.objects.create(
                            name = name,
                            weightage = weightage,
                            asset = asset,
                            amount_invested = amount_invested,
                            current_value = current_value
                        )
            else:
                remaining_weightage = 100 - existing_instruments_weightage_sum
                raise JsonableError(_("Instrument weightage cannot exceed "+str(remaining_weightage)+"%."))
        else:
            raise JsonableError(_("User does not have permissions to this asset group"))
    else:
        raise JsonableError(_("Instrument already exists for given name and assetgroup combination"))
    return result

def get_instruments_weightage_sum(asset : AssetGroup):
    existing_instruments = Instrument.objects.filter(asset = asset)
    if existing_instruments.count() == 0:
        existing_instruments_weightage_sum = 0
    else:
        existing_instruments_weightage_sum = existing_instruments.aggregate(Sum('weightage')).get("weightage__sum")  
    return  existing_instruments_weightage_sum
    

