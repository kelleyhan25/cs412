from django import forms 
from .models import *

class CreateInvestmentForm(forms.ModelForm):
    '''a form to add an investment etf to the database.'''

    class Meta: 
        '''associate this form with a model from database.'''
        model = Investment
        fields = ['shares_owned']

class CreateCompanyInvestmentForm(forms.ModelForm):
    '''a form to add an investment company to the database'''

    class Meta: 
        '''associate this form with a model from database'''
        model = InvestmentCompany
        fields = ['shares_purchased']

class CreateAccountForm(forms.ModelForm):
    '''a form to create a new account and associate it w a customer'''
    first_name = forms.CharField(label="First Name", required=True)
    last_name = forms.CharField(label="Last Name", required=True)
    email = forms.EmailField(label="Email", required=True)
    dob = forms.DateField(label="Date of Birth", required=True)
    account_balance = forms.DecimalField(label="Account Balance", required=True)

    class Meta: 
        '''associate the form with a model from the database'''
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'dob', 'account_balance',]

class UpdateAccountForm(forms.ModelForm):
    '''a form to update an account to the database'''

    class Meta:
        '''associate this form with the account model'''
        model = Customer 
        fields = ['first_name', 'last_name', 'email', 'dob', 'account_balance',]