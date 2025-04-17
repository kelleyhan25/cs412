from django.shortcuts import render
from django.urls import reverse
from django.views.generic import *
from .models import *
from .models import Company, get_stock_price, get_percent_change, format_price_change
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateInvestmentForm, CreateCompanyInvestmentForm, CreateAccountForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from django.contrib.auth import login 


# Create your views here.
class RegistrationView(CreateView):
    '''account regisration view'''
    template_name = 'project/register.html'
    form_class = CreateAccountForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usercreationform'] = UserCreationForm()
        return context
    
    def form_valid(self, form):
        '''reconstruct usercreationform from post data'''
        user_form = UserCreationForm(self.request.POST)
        user = user_form.save()

        form.instance.user = user
        account_balance = form.cleaned_data['account_balance']
        form.instance.cash_value = account_balance
        form.instance.stock_value = 0

        return super().form_valid(form)
    
    def get_success_url(self):
        '''url to redirect to after creating a new user'''
        return reverse('login')
    
class BrowseETFsView(ListView):
    '''view to display all ETFs'''
    template_name = 'project/browse.html'
    model = Bucket
    context_object_name = 'buckets'

class BuyETFShares(LoginRequiredMixin, DetailView, CreateView):
    '''a view to buy an etf share and add an investment to the database'''
    template_name = 'project/buy_shares.html'
    model = Bucket
    form_class = CreateInvestmentForm
    context_object_name = 'bucket'

    def get_success_url(self):
        '''redirects to my investments page after purchase'''
        return reverse('my_investments')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        bucket = Bucket.objects.get(pk=pk)

        bucket_companies = BucketCompany.objects.filter(bucket=bucket)
        context['bucket_companies'] = bucket_companies
        return context
    
    def form_valid(self, form):
        '''investment -> user'''
        customer = Customer.objects.get(user=self.request.user)
        form.instance.customer = customer 
        pk = self.kwargs['pk']
        bucket = Bucket.objects.get(pk=pk)
        form.instance.bucket = bucket

        shares = form.cleaned_data['shares_owned']
        total_cost = shares * bucket.price_per_share

        if customer.cash_value < total_cost: 
            form.add_error(None, "Insufficient funds")
            return self.form_invalid(form)
        
        customer.cash_value -= total_cost
        customer.stock_value += total_cost
        customer.save()

        return super().form_valid(form)
    
    def get_login_url(self):
        '''return url required for login'''
        return reverse('login')



class CompanyDetailView(LoginRequiredMixin, CreateView, DetailView):
    '''a view to display a singular company and its updated stock prices and % change and buy shares'''
    template_name = 'project/company.html'
    model = Company
    context_object_name = 'company'
    form_class = CreateCompanyInvestmentForm

    def get_success_url(self):
        '''redirects to my investments page after purchase'''
        return reverse('my_investments')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        company = context['company']
        company.update_stock_price()
        change = get_percent_change(company.stock_symbol)
        formatted_change = format_price_change(change)
        
        context['formatted_change'] = formatted_change
        
        return context
    
    def form_valid(self, form):
        '''investment -> user'''
        customer = Customer.objects.get(user=self.request.user)
        form.instance.customer = customer
        pk = self.kwargs['pk']
        company = Company.objects.get(pk=pk)
        form.instance.company = company 
        shares = form.cleaned_data['shares_purchased']
        total_cost = shares * company.stock_price

        if customer.cash_value < total_cost:
            form.add_error(None, "Insufficient funds")
            return self.form_invalid(form)
        
        customer.cash_value -= total_cost
        customer.stock_value += total_cost
        customer.save()
        return super().form_valid(form)
    
    def get_login_url(self):
        return reverse('login')

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
    context_object_name = 'customer'

    def get_object(self):
        '''method for customer lookup in URL w/out pk'''
        return Customer.objects.get(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.get_object()
        context['customer'] = customer 
        my_investments = customer.get_investments()
        context['my_investments'] = my_investments
        company_investments = customer.getCompanyInvestments()
        context['company_investments'] = company_investments
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