from django import forms 
from .models import *

class CreateInvestmentForm(forms.ModelForm):
    '''a form to add an investment to the database.'''

    class Meta: 
        '''associate this form with a model from database.'''
        model = Investment
        fields = ['shares_owned']