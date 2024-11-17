from django.db import models
from django.db.models import Sum
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from apps.home.lib import backend,operations
import hashlib

DECIMAL_MAX_DIGITS = 8

COUNTRIES = [
    ('IN', 'India'),
    ('US', 'United States'),
    ('CN', 'China'),
    ('JP', 'Japan'),
    ('HK', 'Hong Kong'),
    ('FR', 'France'),
    ('UK', 'United Kingdom'),
    ('CA', 'Canada'),
    ('KR', 'South Korea'),
    ('TW', 'Taiwan'),
    ('CH', 'Switzerland'),
    ('AU', 'Australia'),
    ('NL', 'Netherlands'),
    ('IR', 'Iran'),
    ('ZA', 'South Africa'),
    ('BR', 'Brazil'),
    ('SE', 'Sweden'),
    ('ES', 'Spain'),
    # add more countries
]

SUBSCRIPTION_TYPES = [
    ("F", "Free"),
    ("P", "Premium")
]

################################################################################################################################
# PDF
################################################################################################################################
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'user_{instance.user.id}/{filename}'

class PDFDocument(models.Model):
    title = models.CharField(max_length=255)  # You can use this to store a title or description of the file
    document = models.FileField(upload_to=user_directory_path)  # 'pdfs/' is the directory in MEDIA_ROOT where files are saved
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Store when the file was uploaded
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_hash = models.CharField(max_length=64, blank=True, null=True)  # To store the file hash
    backend_doc_id = models.IntegerField(blank=True, null=True)  # To store the document id in backend
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.file_hash:
            self.file_hash = self.calculate_file_hash()
        super().save(*args, **kwargs)

    def calculate_file_hash(self):
        hash_md5 = hashlib.md5()
        for chunk in self.document.chunks():
            hash_md5.update(chunk)
        return hash_md5.hexdigest()

class PDFDocumentStatus(models.Model):
    STATUS_CHOICES = [
        ('uploaded', 'Uploaded'),
        ('processing', 'Processing'),
        ('processed', 'Processed'),
        ('failure', 'Failure'),
    ]

    document = models.ForeignKey(PDFDocument, on_delete=models.CASCADE, related_name='statuses')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=True, null=True)  # Optional message for errors or additional info

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.document.title} - {self.status} at {self.timestamp}"

################################################################################################################################
# Nominee
################################################################################################################################
class UserNominee(models.Model):
    STATUS_CHOICES = [
        ("A", "Active"),
        ("U", "Unsubscribed")
    ]
    id: int = models.AutoField(auto_created=True, primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=120, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="A")

    def __str__(self) -> str:
         return self.name
    
################################################################################################################################
# User
################################################################################################################################
class UserProfile(models.Model):
    id: int = models.AutoField(auto_created=True, primary_key=True, verbose_name="ID")
    first_name = models.CharField(max_length=120, null=True, blank=True)
    last_name = models.CharField(max_length=120, null=True, blank=True)
    address = models.CharField(max_length=120, null=True, blank=True)
    bio = models.CharField(max_length=500, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=4, choices=COUNTRIES)
    subscription_type = models.CharField(max_length=20, choices=SUBSCRIPTION_TYPES, default="F")

################################################################################################################################
# Tour
################################################################################################################################
class UserTour(models.Model):
    STATUS_CHOICES = [
        ("Not-Started", "Not-Started"),
        ("In-Progress", "In-Progress"),
        ("Completed", "Completed"),
    ]
    id = models.AutoField(auto_created=True, primary_key=True, verbose_name="ID")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Not-Started")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

################################################################################################################################
# TourStep
################################################################################################################################
class UserTourStep(models.Model):
    STATUS_CHOICES = [
        ("Not-Started", "Not-Started"),
        ("In-Progress", "In-Progress"),
        ("Completed", "Completed"),
    ]
    id = models.AutoField(auto_created=True, primary_key=True, verbose_name="ID")
    step_name = models.CharField(max_length=120, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,default="Not-Started")
    tour = models.ForeignKey(UserTour, on_delete=models.CASCADE)

################################################################################################################################
# Investment Summary
################################################################################################################################
class Networth(models.Model):
    id: int = models.AutoField(auto_created=True, primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=120, null=True, blank=True)
    amount = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

    def get_total_weightage_used(self):
        result = 0
        categories = Category.objects.filter(networth = self)
        for category in categories:
            result += category.weightage
        
        if result is not None:
            result = round(result,2)
        return result
    
    @property
    def get_base_unit(self):
        return BaseUnit.objects.get(networth = self)
    
    @property
    def current_value(self):
        categories = Category.objects.filter(networth=self)
        result = 0
        for category in categories:
            if category.current_value > 0:
                result =  result + category.current_value
            else:
                result = 0
                break
        result = operations.round_amount_based_on_base_unit(result,self.get_base_unit.value)
        return result
    
    def __str__(self) -> str:
         return self.name

class BaseUnit(models.Model):
    id: int = models.AutoField(auto_created=True, primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=200)
    value = models.IntegerField()
    networth = models.OneToOneField(Networth, on_delete=models.CASCADE)

    def __str__(self) -> str:
         return self.name    

class Category(models.Model):
    id: int = models.AutoField(auto_created=True, primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=200)
    weightage = models.IntegerField()
    networth = models.ForeignKey(Networth, on_delete=models.CASCADE)
    display_amount_in_base_unit = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def get_total_weightage_used(self):
        result = 0
        assetgroups = AssetGroup.objects.filter(category = self)
        for assetgroup in assetgroups:
            result += assetgroup.weightage
        
        if result is not None:
            result = round(result,2)
        return result

    def get_total_invested_amount(self):
        amount = 0
        assets = AssetGroup.objects.filter(category = self)
        networth = self.networth
        base_unit = BaseUnit.objects.get(networth=networth)
        for asset in assets:
            instruments = Instrument.objects.filter(asset = asset)
            if instruments.count() > 0:
                amount += instruments.aggregate(Sum('amount_invested')).get('amount_invested__sum')
        if amount is not None:
            check_result = operations.check_if_amount_is_less_one_percent_than_base_unit(amount, base_unit.value)
            if check_result:                
               amount = operations.round_amount_based_on_base_unit(amount/base_unit.value, base_unit.value)
            else:
                amount = round(amount/base_unit.value,2)
        return amount

    def get_diff(self):
        if self.get_category_allocation() ==0:
            result = self.get_total_invested_amount()
        else: 
            result = (self.get_total_invested_amount()/self.get_category_allocation())*100
        return round(result,2)

    def get_category_allocation(self):
        result = (self.networth.amount*self.weightage)/100
        baseunit = BaseUnit.objects.get(networth = self.networth)
        return backend.get_allocation(result,baseunit,self.display_amount_in_base_unit)
    
    @property
    def pnl_amount(self):
        result = 0
        if self.current_value >= 0:
            result = ((self.current_value/self.get_base_unit.value) - self.get_total_invested_amount())
        else:
            result = 0
        result = operations.get_amount_in_digits(result)
        return result

    @property
    def pnl_percentage(self):
        if self.current_value > 0 and self.get_total_invested_amount() > 0:
            result = (((self.current_value/self.get_base_unit.value) - self.get_total_invested_amount())/self.get_total_invested_amount())*100
        else:
            result = 0
        result = operations.get_amount_in_digits(result)
        return result

    def __str__(self) -> str:
         return self.name

    def __str__(self) -> str:  
         return self.name
        
    @property
    def current_value(self):
        assets = AssetGroup.objects.filter(category=self)
        result = 0
        for asset in assets:
            if asset.current_value >= 0:
                result =  result + asset.current_value
            else:
                result = 0
                break
        return result
    
    @property
    def get_base_unit(self):
        return BaseUnit.objects.get(networth = self.networth)

    @property
    def current_value_in_units(self):
        result = 0
        unit_value = self.get_base_unit.value
        result = operations.round_amount_based_on_base_unit((self.current_value/unit_value),self.get_base_unit.value)
        result = operations.get_amount_in_digits(result)
        return result

class AssetGroup(models.Model):
    id: int = models.AutoField(auto_created=True, primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=200)
    weightage = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    display_amount_in_base_unit = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def get_total_weightage_used(self):
        result = 0
        instruments = Instrument.objects.filter(asset = self)
        for instrument in instruments:
            result += instrument.weightage
        
        if result is not None:
            result = round(result,2)
        return result

    def get_diff(self):
        if self.total_invested_amount is not None :
            result = (self.total_invested_amount/self.get_asset_allocation())*100
        else:
            result = 0
        return round(result,2)

    def get_asset_allocation(self):
        result = (self.category.get_category_allocation()*self.weightage)/100
        baseunit = self.category.networth.baseunit
        result = backend.get_allocation(result,baseunit,self.display_amount_in_base_unit)
        result = operations.get_amount_in_digits(result)
        return result
    
    @property
    def current_value(self):
        instruments = Instrument.objects.filter(asset=self)
        result = 0
        for instrument in instruments:
            if instrument.current_value > 0:
                result =  result + instrument.current_value
            else:
                result = 0
                break
        result = operations.get_amount_in_digits(result)
        return result
    
    @property
    def get_base_unit(self):
        return BaseUnit.objects.get(networth = self.category.networth)

    @property
    def current_value_in_units(self):
        result = 0
        unit_value = self.get_base_unit.value
        result = operations.round_amount_based_on_base_unit((self.current_value/unit_value), self.get_base_unit.value)
        result = operations.get_amount_in_digits(result)
        return result


    @property
    def total_invested_amount(self):
        instruments = Instrument.objects.filter(asset = self)
        networth = self.category.networth
        base_unit = BaseUnit.objects.get(networth=networth)
        amount = instruments.aggregate(Sum('amount_invested')).get('amount_invested__sum')
        if amount is not None:
            amount = round(amount/base_unit.value,3)
            amount = operations.get_amount_in_digits(amount)
        else:
            amount = 0
        return amount

    @property
    def pnl_amount(self):
        networth = self.category.networth
        base_unit = BaseUnit.objects.get(networth=networth)
        if self.current_value > 0:
            amount = self.current_value
            amount = round(amount/base_unit.value,3)
            result = (amount - self.total_invested_amount)
        else:
            result = 0
        result = operations.get_amount_in_digits(result)
        return result

    @property
    def pnl_percentage(self):
        networth = self.category.networth
        base_unit = BaseUnit.objects.get(networth=networth)
        if self.current_value > 0 and self.total_invested_amount> 0:
            amount = self.current_value
            amount = round(amount/base_unit.value,3)
            result = ((amount - self.total_invested_amount)/self.total_invested_amount)*100
        else:
            result = 0
        result = operations.get_amount_in_digits(result)
        return result

    def __str__(self) -> str:
         return self.name
    
         
class Instrument(models.Model):
    id: int = models.AutoField(auto_created=True, primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=200)
    weightage = models.IntegerField(default=0)
    amount_invested = models.IntegerField()
    current_value = models.IntegerField(default=0)
    asset = models.ForeignKey(AssetGroup, on_delete=models.CASCADE)
    display_amount_in_base_unit = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    
    @property
    def get_baseunit(self):
        return self.asset.category.networth.baseunit

    def get_instrument_allocation(self):
        result = (self.asset.get_asset_allocation()*self.weightage)/100
        if result <= 1:
            result = 1
        baseunit = self.get_baseunit
        return backend.get_allocation(result,baseunit,self.display_amount_in_base_unit)

    @property
    def total_invested_amount(self):
        baseunit = self.get_baseunit
        amount = self.amount_invested
        if amount is not None:
            amount = round(amount/baseunit.value,2)
        return amount
    
    @property
    def pnl_amount(self):
        if self.current_value > 0:
            result = (self.current_value - self.amount_invested)
        else:
            result = 0
        result = round(result,2)
        return result
    
    @property
    def pnl_percentage(self):
        if self.current_value > 0 and self.amount_invested> 0:
            result = ((self.current_value - self.amount_invested)/self.amount_invested)*100
        else:
            result = 0
        return round(result,0)

    def __str__(self) -> str:
         return self.name
    

################################################################################################################################
# Backup Tables
################################################################################################################################
class Backup(models.Model):
    STATUS_CHOICES = [
        ("Not-Started", "Not-Started"),
        ("In-Progress", "In-Progress"),
        ("Completed", "Completed"),
        ("Deleted", "Deleted"),
    ]
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Not-Started")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

class NetworthBackup(models.Model):
    src_networth_id=models.IntegerField()
    name = models.CharField(max_length=120, null=True, blank=True)
    amount = models.IntegerField()
    user = models.IntegerField()
    is_active = models.BooleanField(default=False)
    backup = models.ForeignKey(Backup, on_delete=models.DO_NOTHING)

class BaseUnitBackup(models.Model):
    name = models.CharField(max_length=200)
    value = models.IntegerField()
    networth = models.IntegerField()
    backup = models.ForeignKey(Backup, on_delete=models.DO_NOTHING)

class CategoryBackup(models.Model):
    src_category_id=models.IntegerField()
    name = models.CharField(max_length=200)
    weightage = models.IntegerField()
    networth = models.IntegerField()
    display_amount_in_base_unit = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    backup = models.ForeignKey(Backup, on_delete=models.DO_NOTHING)

class AssetGroupBackup(models.Model):
    src_asset_id=models.IntegerField()
    name = models.CharField(max_length=200)
    weightage = models.IntegerField()
    category = models.IntegerField()
    display_amount_in_base_unit = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    backup = models.ForeignKey(Backup, on_delete=models.DO_NOTHING)

class InstrumentBackup(models.Model):
    src_instrument_id=models.IntegerField()
    name = models.CharField(max_length=200)
    weightage = models.IntegerField()
    amount_invested = models.IntegerField()
    current_value = models.IntegerField()
    asset = models.IntegerField()
    display_amount_in_base_unit = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)
    backup = models.ForeignKey(Backup, on_delete=models.DO_NOTHING)