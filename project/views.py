from django.shortcuts import render
from django.urls import reverse
from django.views.generic import *
from .models import *
from .models import Company, get_stock_price, get_percent_change, format_price_change
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateInvestmentForm, CreateCompanyInvestmentForm, CreateAccountForm, UpdateAccountForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from django.contrib.auth import login 
from django.utils.timesince import timesince
from datetime import datetime, timedelta 
import plotly 
import plotly.graph_objs as go 

# Create your views here.

class HomePageView(DetailView):
    '''a view to display the homepage and summary'''
    template_name = 'project/home.html'
    model = Customer 
    context_object_name = 'homepage'

    def get_object(self):
        '''return the currently logged in user account info'''
        return Customer.objects.get(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dowjones = get_stock_price("^DJI")
        djchange = format_price_change(get_percent_change("^DJI"))
        sp500 = get_stock_price("^GSPC")
        spchange = format_price_change(get_percent_change("^GSPC"))
        nasdaqusd = get_stock_price("^IXIC")
        nchange = format_price_change(get_percent_change("^IXIC"))
        context['nasdaqusd'] = nasdaqusd
        context['nchange'] = nchange
        context['sp500'] = sp500
        context['spchange'] = spchange
        context['djchange'] = djchange
        context['dowjones'] = dowjones
        customer = self.get_object()
        account_balance = customer.account_balance
        context['account_balance'] = account_balance

        # the sample code provided when learning about how to make graphs on blackboard did not work, so i had to google and read the plotly documentation to figure out how to do it
        # needed a trace, which is the data list 
        # https://plotly.com/python/reference/scatter/
        #https://plotly.com/python/creating-and-updating-figures/
        nasdaq = yf.Ticker("^IXIC")
        data = nasdaq.history(period="30d")
        x = data.index # dates 
        y = data['Close'] # stock closing prices 

        fig = go.Figure() 
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Closing Price'))

        fig.update_layout(
            title="NASDAQ Stock Price (Last 30 Days)",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            height=350,
        )

        graph_div_scatter = plotly.offline.plot(
            {"data": fig.data, 
             "layout": fig.layout},
             auto_open=False,
             output_type="div"
        )

        context['graph_div_scatter'] = graph_div_scatter

        return context
    


class RegistrationView(CreateView):
    '''account registration view'''
    template_name = 'project/register.html'
    form_class = CreateAccountForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usercreationform'] = UserCreationForm()
        return context
    
    def form_valid(self, form):
        '''reconstruct usercreationform from post data'''
        user_form = UserCreationForm(self.request.POST)
 
        if user_form.is_valid():
            user = user_form.save()
            login(self.request, user)
            form.instance.user = user
            account_balance = form.cleaned_data['account_balance']
            form.instance.cash_value = account_balance
            form.instance.stock_value = 0
            
            return super().form_valid(form)
        else: #couldn't figure out why just the above code wasn't working, stack overflow led me to this https://docs.djangoproject.com/en/3.1/ref/forms/api/#django.forms.Form.add_error and the below else block
            print(f"UserCreationForm errors: {user_form.errors}")
            for field, errors in user_form.errors.items():
                for error in errors:
                    form.add_error(None, f"{field}: {error}")
            
            return self.form_invalid(form)
    
    def get_success_url(self):
        return reverse('my_investments')
    
class BrowseETFsView(ListView):
    '''view to display all ETFs'''
    template_name = 'project/browse.html'
    model = Bucket
    context_object_name = 'buckets'

    def get_queryset(self):
        queryset = super().get_queryset()
        for bucket in queryset:
            bucket.update_price_per_share()
        return queryset 

class SellETFShares(LoginRequiredMixin, DeleteView):
    '''a view to sell an etf share and delete the investment from the database'''
    template_name = 'project/sell_shares.html'
    model = Investment
    context_object_name = 'investment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        investment = self.get_object()
        investment.bucket.update_price_per_share()

        shares = investment.shares_owned 
        price = investment.bucket.price_per_share 
        context['total_value'] = round(Decimal(str(shares)) * Decimal(str(price)), 2) 
        return context 
    

    def get_success_url(self):
        '''return a url for redirection after selling'''
        return reverse('my_investments')
    
    def form_valid(self, form):
        '''method where i can process during POST and update account balance'''
        self.object = self.get_object()
        print("form valid called")
        self.object.bucket.update_price_per_share()
        print("about to call sell")
        self.object.sell()
        print("after calling sell")

        return super().form_valid(form)

class SellCompanyShares(LoginRequiredMixin, DeleteView):
    '''a view to sell a company share and delete the investment from the database'''
    template_name = 'project/sell_shares.html'
    model = InvestmentCompany
    context_object_name = 'investment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        investment = self.get_object()
        investment.company.update_stock_price()

        shares = investment.shares_purchased
        price = investment.company.stock_price 
        context['total_value'] = round(Decimal(str(shares)) * Decimal(str(price)), 2)
        return context 
    

    def get_success_url(self):
        '''return a url for redirection after selling'''
        return reverse('my_investments')
    

    def form_valid(self, form):
        '''method where i can process during POST and update account balance'''
        self.object = self.get_object()
        print("form valid called")
        self.object.company.update_stock_price()
        print("about to call sell")
        self.object.sell()
        print("after calling sell")
        return super().form_valid(form)
    
    

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

        if bucket.last_updated:
            context['price_last_updated'] = timesince(bucket.last_updated) + ' ago'
        else:
            context['price_last_updated'] = 'Not available'
        return context
    
    def form_valid(self, form):
        '''investment -> user'''
        customer = Customer.objects.get(user=self.request.user)
        form.instance.customer = customer 
        pk = self.kwargs['pk']
        bucket = Bucket.objects.get(pk=pk)
        bucket.update_price_per_share()
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
            industry = self.request.GET['industry'].strip()
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
        customer = Customer.objects.get(user=self.request.user)
        customer.update_balances()
        return customer
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = Customer.objects.get(user=self.request.user)
        context['customer'] = customer
        my_investments = customer.get_investments()
        context['my_investments'] = my_investments
        company_investments = customer.getCompanyInvestments()
        context['company_investments'] = company_investments
        user = self.request.user 
        context['user'] = user 

        if customer.last_updated:
            context['last_updated'] = timesince(customer.last_updated) + ' ago'
        else: 
            context['last_updated'] = 'Not available'
        return context

    def get_login_url(self):
        '''return the URL required for login'''
        return reverse('login')

class AccountDetailView(LoginRequiredMixin, DetailView, UpdateView):
    '''a view to display the account details'''
    form_class = UpdateAccountForm
    template_name = 'project/account.html'
    model = Customer
    context_object_name = 'account'
    

    def get_object(self):
        '''return the currently logged in user account info'''
        return Customer.objects.get(user=self.request.user)

    def get_login_url(self):
        '''return the URL required for login'''
        return reverse('login')
    
    def form_valid(self, form):
        '''handle the form submission to update account'''
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('account')