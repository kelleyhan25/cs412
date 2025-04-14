from django.shortcuts import render
from django.views.generic import *
from .models import *

# Create your views here.
class BrowseETFsView(ListView):
    '''view to display all ETFs'''
    template_name = 'project/browse.html'
    model = Bucket
    context_object_name = 'buckets'


class CompaniesListView(ListView):
    '''view to display all the companies'''
    template_name = 'project/companies.html'
    model = Company
    context_object_name = 'companies'