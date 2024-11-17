from django import forms
from django.core.exceptions import ValidationError
import re
from apps.home.lib import constants
from apps.home.lib.common import Validators
from apps.home.models import PDFDocument

class PDFDocumentForm(forms.ModelForm):
    class Meta:
        model = PDFDocument
        fields = ['title', 'document']  # Match the fields with your model
    

class BackupForm(forms.Form):
    name = forms.CharField(max_length=120)
    status = forms.CharField(max_length=120, required=False)

    def clean_name(self):
        name = self.cleaned_data['name']
        if not re.match(r'^[a-zA-Z0-9_\- ]+$', name):
            raise forms.ValidationError("Backup Name must contain only letters, numbers, underscores or hyphens.")
        return name

    

class UserNomineeForm(forms.Form):
    
    name = forms.CharField(max_length=200, label="Nominee Name")
    email = forms.EmailField(error_messages={'invalid': 'Please enter a valid email address.'})

    def clean_name(self):
        name = self.cleaned_data['name']
        if not re.match(constants.names_regex, name):
            raise forms.ValidationError("Nominee Name must contain only letters")
        return name
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if not re.match(constants.email_regex, email):
                raise forms.ValidationError("Invalid email. Provided email is not valid")
        return email


class NetworthForm(forms.Form):
    name = forms.CharField(max_length=120, required=False)
    amount = forms.IntegerField(error_messages={'invalid': 'Amount must contain only numbers.'})

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

class UserProfileForm(forms.Form):
    first_name = forms.CharField(max_length=120, required=False)
    last_name = forms.CharField(max_length=120, required=False)
    address = forms.CharField(max_length=120, required=False)
    bio = forms.CharField(max_length=120, required=False, validators=[Validators.validate_no_tags,Validators.validate_no_sql_statements])

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if first_name != '':
            if not re.match(constants.names_regex, first_name):
                raise forms.ValidationError("Invalid first name. First name must contain only letters")
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if last_name != '':
            if not re.match(constants.names_regex, last_name):
                raise forms.ValidationError("Invalid last name. Last name must contain only letters")
        return last_name

    def clean_address(self):
        address = self.cleaned_data['address']
        if address != '':
            if not re.match(constants.address_regex, address):
                raise forms.ValidationError("Invalid address. The address should only contain alphanumeric characters, whitespace, hyphens, dots, commas, and hash characters.")
        return address
    
    def clean_bio(self):
        bio = self.cleaned_data['bio']
        if bio != '': 
            Validators.validate_no_tags(bio)
            Validators.validate_no_sql_statements(bio)
        return bio

    
