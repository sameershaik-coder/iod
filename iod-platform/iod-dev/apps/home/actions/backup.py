
from apps.home.models import(
    BaseUnit,
    Networth
    )
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.db import transaction
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
import logging

logger = logging.getLogger(__name__)

def check_eligibility_for_backup(user):
    result = False
    try:
        networth = Networth.objects.get(user=user,is_active=True)
        category_data = Category.objects.filter(networth=networth)
        for category in category_data:
            assetgroup_data = AssetGroup.objects.filter(category=category)
            for asset in assetgroup_data:
                instruments_data = Instrument.objects.filter(asset=asset)
                for instrument in instruments_data:
                    if(
                        instrument.current_value !=0
                        and instrument.amount_invested !=0
                        and instrument.weightage !=0
                        ):
                        result=True
                        break
    except Exception as e:
        logger.error(e)
    return result
                
def get_backup_by_id(id:int, user:User):
    return Backup.objects.get(id=id,user=user, status="Completed")

def get_completed_backups(user:User):
    return Backup.objects.filter(user=user, status="Completed")                

def get_backup_by_name(user:User, name:str):
    return Backup.objects.get(user=user,name=name)

def get_backups(user:User):
    return Backup.objects.filter(user=user)

def restore_backup(user:User,backup_id:int):
    result=False
    backup=Backup.objects.get(id=backup_id, user=user)
    with transaction.atomic():
        try:
            networth_data = NetworthBackup.objects.filter(user=user.id,backup=backup)
            for networth in networth_data:
                # Delete existing data for the user
                Networth.objects.filter(user=user).delete()
                
                # restore the networth
                r_networth = Networth.objects.create(
                name=networth.name,
                amount=networth.amount,
                user=user,
                is_active=networth.is_active
                 )
                
                #delete existing base units for user
                BaseUnit.objects.filter(networth=networth.src_networth_id).delete()

                baseunit_data = BaseUnitBackup.objects.get(networth=networth.src_networth_id,backup=backup)

                # create a base unit from backup
                base_unit = BaseUnit.objects.create(
                    name=baseunit_data.name,
                    value=baseunit_data.value,
                    networth=r_networth
                )

                category_data = CategoryBackup.objects.filter(networth=networth.src_networth_id, src_category_id__gt=0)
                for category in category_data:
                    #Category.objects.filter(networth=networth.src_networth_id).delete()
                    r_category = Category.objects.create(
                    name=category.name,
                    weightage=category.weightage,
                    networth=r_networth,
                    display_amount_in_base_unit=category.display_amount_in_base_unit,
                    is_active=category.is_active
                    )
                    
                    assetgroup_data = AssetGroupBackup.objects.filter(category=category.src_category_id, src_asset_id__gt=0)
                    for asset in assetgroup_data:
                        #AssetGroup.objects.filter(category=category.src_category_id).delete()
                        r_asset = AssetGroup.objects.create(
                        name=asset.name,
                        weightage=asset.weightage,
                        category=r_category,
                        display_amount_in_base_unit=asset.display_amount_in_base_unit,
                        is_active=asset.is_active
                        )
                        
                        instruments_data = InstrumentBackup.objects.filter(asset=asset.src_asset_id, src_instrument_id__gt=0)
                        for instrument in instruments_data:
                            #Instrument.objects.filter(asset=r_asset).delete()
                            Instrument.objects.create(
                            name=instrument.name,
                            weightage=instrument.weightage,
                            amount_invested = instrument.amount_invested,
                            current_value = instrument.current_value,
                            asset=r_asset,
                            display_amount_in_base_unit=instrument.display_amount_in_base_unit,
                            is_active=instrument.is_active
                            )
            result=True        
                        
        except Exception as e:
            result=False
            # Rollback the transaction in case of any exception
            transaction.set_rollback(True)
            # Optionally, handle or log the exception
            print(f"Error occurred during backup restoration: {e}")
            logger.error(f"[ACTIONSBACKUP] : There was an error during backup restore operation for user : {user.id} and backup id : {backup_id} with following exception {e}")

    return result    

# def clean_backup():
#     with transaction.atomic():
#         InstrumentBackup.objects.all().delete()
#         AssetGroupBackup.objects.all().delete()
#         CategoryBackup.objects.all().delete()
#         NetworthBackup.objects.all().delete()
#         Backup.objects.all().delete()
#         print("Delete all backup data")

def do_edit_backup(user:User,backup_id:int,name):
    backup=Backup.objects.get(id=backup_id, user=user)
    with transaction.atomic():
        backup.name=name
        backup.save()

def do_delete_backup(user:User,backup_id:int):
    backup=Backup.objects.get(id=backup_id)
    with transaction.atomic():
        networth_data = NetworthBackup.objects.filter(user=user.id,backup=backup)
        for networth in networth_data:
            category_data = CategoryBackup.objects.filter(networth=networth.src_networth_id, src_category_id__gt=0)
            for category in category_data:
                assetgroup_data = AssetGroupBackup.objects.filter(category=category.src_category_id, src_asset_id__gt=0)
                for asset in assetgroup_data:
                    instruments_data = InstrumentBackup.objects.filter(asset=asset.src_asset_id, src_instrument_id__gt=0)
                    for instrument in instruments_data:
                        instrument.delete()
                    asset.delete()
                category.delete()
            networth.delete()
        backup.status="Deleted"
        backup.save()

def do_create_backup(user:User,name:str)-> bool:
    with transaction.atomic():
        networth_data = Networth.objects.filter(user=user,is_active=True)

        # Create a new backup instance
        backup = Backup.objects.create(name=name,status='Not-Started', user=user)  # Assuming Backup model has a 'user' field

        # Backup Networth data
        for item in networth_data:
            networth = NetworthBackup.objects.create(
                src_networth_id=item.id,
                name=item.name,
                amount=item.amount,
                user=item.user.id,
                is_active=item.is_active,
                backup=backup
            )
            base_unit_data=BaseUnit.objects.get(networth=item)
            BaseUnitBackup.objects.create(
                name=base_unit_data.name,
                value=base_unit_data.value,
                networth=base_unit_data.networth.id,
                backup=backup
            )
            category_data = Category.objects.filter(networth=item.id)
            for item in category_data:
                category = CategoryBackup.objects.create(
                    src_category_id=item.id,
                    name=item.name,
                    weightage=item.weightage,
                    networth=item.networth.id,
                    display_amount_in_base_unit=item.display_amount_in_base_unit,
                    is_active=item.is_active,
                    backup=backup
                )
                assetgroup_data = AssetGroup.objects.filter(category=item.id)
                for item in assetgroup_data:
                    asset = AssetGroupBackup.objects.create(
                        src_asset_id=item.id,
                        name=item.name,
                        weightage=item.weightage,
                        category=item.category.id,
                        display_amount_in_base_unit=item.display_amount_in_base_unit,
                        is_active=item.is_active,
                        backup=backup
                    )
                    instruments_data = Instrument.objects.filter(asset=item.id)
                    for item in instruments_data:
                        instrument = InstrumentBackup.objects.create(
                            src_instrument_id=item.id,
                            name=item.name,
                            weightage=item.weightage,
                            amount_invested = item.amount_invested,
                            current_value = item.current_value,
                            asset=item.asset.id,
                            display_amount_in_base_unit=item.display_amount_in_base_unit,
                            is_active=item.is_active,
                            backup=backup
                        )

        backup.status="Completed"
        backup.save()