from django import forms
import re

class InstrumentForm(forms.Form):
    
    name = forms.CharField(max_length=200, label="Instrument Name")
    amount_invested = forms.IntegerField(error_messages={'invalid': 'Amount invested must contain only numbers.'})
    current_value = forms.IntegerField(error_messages={'invalid': 'Current Value must contain only numbers'})

    def clean_name(self):
        name = self.cleaned_data['name']
        if not re.match(r'^[a-zA-Z0-9_\- ]+$', name):
            raise forms.ValidationError("Instrument Name must contain only letters, numbers, underscores or hyphens.")
        return name
    
    def clean_amount_invested(self):
        amount_invested = self.cleaned_data['amount_invested']
        if amount_invested <= 0:
            raise forms.ValidationError("Amount Invested must be greater than zero.")
        return amount_invested
    
    def clean_current_value(self):
        current_value = self.cleaned_data['current_value']
        if current_value <= 0:
            raise forms.ValidationError("Current Value must be greater than zero.")
        return current_value

class AssetGroupForm(forms.Form):
    
    name = forms.CharField(max_length=200, label="Asset-Group Name")
    weightage = forms.IntegerField(error_messages={'invalid': 'Asset Group Weightage must contain only numbers'})

    def clean_name(self):
        name = self.cleaned_data['name']
        if not re.match(r'^[a-zA-Z0-9_\- ]+$', name):
            raise forms.ValidationError("Asset-Group Name must contain only letters, numbers, underscores or hyphens.")
        return name
    
    def clean_weightage(self):
        weightage = self.cleaned_data['weightage']
        if weightage <= 0:
            raise forms.ValidationError("Weightage must be greater than zero.")
        return weightage

class CategoryForm(forms.Form):
    
    name = forms.CharField(max_length=200, label="Category Name")
    weightage = forms.IntegerField(error_messages={'invalid': 'Category Weightage must contain only numbers'})

    def clean_name(self):
        name = self.cleaned_data['name']
        if not re.match(r'^[a-zA-Z0-9_\- ]+$', name):
            raise forms.ValidationError("Category Name must contain only letters, numbers, underscores or hyphens.")
        return name
    
    def clean_weightage(self):
        weightage = self.cleaned_data['weightage']
        if weightage <= 0:
            raise forms.ValidationError("Weightage must be greater than zero.")
        return weightage

class AssetTypeForm(forms.Form):
    
    name = forms.CharField(max_length=200, label="Asset-Type Name")
    weightage = forms.IntegerField(error_messages={'invalid': 'Please enter a valid integer.'})

    def clean_name(self):
        name = self.cleaned_data['name']
        if not re.match(r'^[a-zA-Z0-9_\- ]+$', name):
            raise forms.ValidationError("Asset-Type Name must contain only letters, numbers, underscores or hyphens.")
        return name
    
    def clean_weightage(self):
        weightage = self.cleaned_data['weightage']
        if weightage <= 0:
            raise forms.ValidationError("Weightage must be greater than zero.")
        return weightage
    
class BaseUnitForm(forms.Form):
    
    name = forms.CharField(max_length=200, label="Base Unit Name")
    value = forms.IntegerField(error_messages={'invalid': 'Base Unit value must contain only numbers'})
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if not re.match(r'^[a-zA-Z0-9_\- ]+$', name):
            raise forms.ValidationError("Base Unit Name must contain only letters, numbers, underscores or hyphens.")
        return name
    
    def clean_value(self):
        value = self.cleaned_data.get('value')  # Get the value or None
        if value <= 0:
            raise forms.ValidationError("Value must be greater than zero.")
        return value


from django import forms
from django.core import validators

class NetworthForm(forms.Form):
    name = forms.CharField(max_length=120, required=False)
    amount = forms.IntegerField()

    def clean_name(self):
        name = self.cleaned_data['name']
        if not re.match(r'^[a-zA-Z0-9_\- ]+$', name):
            raise forms.ValidationError("Networth Name must contain only letters, numbers, underscores or hyphens.")
        return name

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        return amount
