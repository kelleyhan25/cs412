from django.shortcuts import render
from django.urls import reverse
from django.views.generic import *
from .models import *
from .models import Company, get_stock_price, get_percent_change, format_price_change
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class BrowseETFsView(ListView):
    '''view to display all ETFs'''
    template_name = 'project/browse.html'
    model = Bucket
    context_object_name = 'buckets'

class CompanyDetailView(DetailView):
    '''a view to display a singular company and its updated stock prices and % change'''
    template_name = 'project/company.html'
    model = Company
    context_object_name = 'company'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = context['company']
        company.update_stock_price()
        change = get_percent_change(company.stock_symbol)
        formatted_change = format_price_change(change)
        
        context['formatted_change'] = formatted_change
        
        return context

class CompaniesListView(ListView):
    '''view to display all the companies'''
    template_name = 'project/companies.html'
    model = Company
    context_object_name = 'companies'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        
        if 'company_name' in self.request.GET: 
            company_name = self.request.GET['company_name']
            if company_name:
                queryset = queryset.filter(company_name=company_name)
        
        if 'stock_symbol' in self.request.GET:
            stock_symbol = self.request.GET['stock_symbol']
            if stock_symbol:
                queryset = queryset.filter(stock_symbol=stock_symbol)

        if 'industry' in self.request.GET:
            industry = self.request.GET['industry']
            if industry: 
                queryset = queryset.filter(industry=industry)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #company_price_list = []
        dowjones = get_stock_price("^DJI")
        djchange = format_price_change(get_percent_change("^DJI"))
        sp500 = get_stock_price("^GSPC")
        spchange = format_price_change(get_percent_change("^GSPC"))
        context['sp500'] = sp500
        context['spchange'] = spchange
        context['djchange'] = djchange
        context['dowjones'] = dowjones
        return context
    


class MyInvestmentsDetailView(LoginRequiredMixin, DetailView):
    '''a view to display the user's investments and data related to it'''
    template_name = 'project/my_investments.html'
    model = Customer
    context_object_name = 'my_investments'

    def get_object(self):
        '''method for customer lookup in URL w/out pk'''
        return Customer.objects.get(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.get_object()
        my_investments = customer.get_investments()
        context['my_investments'] = my_investments
        user = self.request.user 
        context['user'] = user 
        return context

    def get_login_url(self):
        '''return the URL required for login'''
        return reverse('login')

class AccountDetailView(LoginRequiredMixin, DetailView):
    '''a view to display the account details'''
    template_name = 'project/account.html'
    model = Customer
    context_object_name = 'account'

    def get_object(self):
        '''return the currently logged in user account info'''
        return Customer.objects.get(user=self.request.user)

    def get_login_url(self):
        '''return the URL required for login'''
        return reverse('login')