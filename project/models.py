# File: models.py 
# Author : Kelley Han kelhan@bu.edu 4/13/25
# Description: All of the models necessary for the ETF Manager project 

from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal 
from django.utils import timezone 
from datetime import timedelta
from . import helper_functions

# Create your models here.
class Customer(models.Model):
    '''encapsulates the idea of a customer and its attributes'''

    # data attributes of a Customer 
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    email = models.EmailField(blank=False)
    dob = models.DateField(blank=False)
    account_balance = models.DecimalField(max_digits=12, decimal_places=2)
    cash_value = models.DecimalField(max_digits=12, decimal_places=2)
    stock_value = models.DecimalField(max_digits=12, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''return a string representation of this Customer object'''
        return f'{self.first_name} {self.last_name}'
    
    def get_investments(self):
        '''returns all the investments the customer has'''
        investments = Investment.objects.filter(customer=self)
        return investments 
    
    def getCompanyInvestments(self):
        '''returns all company investments a customer has'''
        companyinvestments = InvestmentCompany.objects.filter(customer=self)
        return companyinvestments
    
    def update_balances(self):
        '''updates a customer's balances based on current stock prices on yfinance api, updates every half hour'''
        # https://medium.com/django-unleashed/python-timedelta-with-examples-and-use-cases-81def9140880
        if self.last_updated and timezone.now() - self.last_updated < timedelta(minutes=30):
            return False 
        
        new_value = Decimal('0.00') 

        # updates the ETF investment values
        for investment in self.get_investments(): 
            investment.bucket.update_price_per_share()
            shares = Decimal(str(investment.shares_owned))
            investment_value = shares * Decimal(str(investment.bucket.price_per_share))
            new_value += investment_value
        
        # updates the company investment values 

        for investment in self.getCompanyInvestments():
            investment.company.update_stock_price()
            shares = Decimal(str(investment.shares_purchased))
            investment_value = shares * Decimal(str(investment.company.stock_price))
            new_value += investment_value
        
        self.stock_value = new_value
        self.account_balance = self.cash_value + self.stock_value
        self.last_updated = timezone.now()
        self.save()
        return True 
   


class Company(models.Model):
    '''encapsulates the idea of a company and its attributes'''

    #data attributes of a company 
    company_name = models.TextField(blank=False)
    stock_symbol = models.CharField(max_length=4)
    market_cap = models.DecimalField(max_digits=15, decimal_places=2)
    industry = models.TextField(blank=False)
    stock_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def update_market_cap(self):
        '''update the market cap with most recent data pulled from yfinance api'''
        cap = helper_functions.get_market_cap(self.stock_symbol)
        if cap is not None: 
            self.market_cap = Decimal(str(cap))
            self.save()
        return self.market_cap

    def update_stock_price(self):
        '''updates stock price with most recent data from yfinance api'''
        price = helper_functions.get_stock_price(self.stock_symbol)
        if price is not None: 
            self.stock_price = Decimal(str(price))
            self.save()
        return self.stock_price
    
   
    def __str__(self):
        '''return a string representation of this Company object'''
        return f'{self.company_name} {self.stock_symbol}'
    
  

class Bucket(models.Model):
    '''encapsulates the idea of a Bucket, which is fractions of a company'''

    #data attributes of a bucket 
    bucket_name = models.TextField(blank=False)
    description = models.TextField(blank=False)
    total_value = models.DecimalField(max_digits=10, decimal_places=2)
    bucket_symbol = models.CharField(max_length=4)
    price_per_share = models.DecimalField(max_digits=10, decimal_places=2)
    last_updated = models.DateTimeField(null=True, blank=True)
    

    def __str__(self):
        '''return a string representation of this Bucket'''
        return f'{self.bucket_name}'
    
    def company_count(self):
        '''returns the number of companies tied to the bucket'''
        return BucketCompany.objects.filter(bucket=self).count()
    
    def update_price_per_share(self):
        '''returns updated bucket price based on yfinance api on the hour'''
        if self.last_updated and timezone.now() - self.last_updated < timedelta(hours=1):
            return self.price_per_share
        
        bucket_companies = BucketCompany.objects.filter(bucket=self)
        weighted_value = 0 

        for b in bucket_companies: 
            b.company.update_stock_price()
            stockprice = Decimal(str(b.company.stock_price))
            percentage = Decimal(str(b.percentage)) / Decimal("100")
            contribution = stockprice * percentage
            weighted_value += contribution
        self.price_per_share = round(weighted_value, 2)
        self.last_updated = timezone.now()
        self.save()
        return self.price_per_share
    
    
    

class BucketCompany(models.Model):
    '''encapsulates the relationship (many to many) with bucket and companies.'''
    bucket = models.ForeignKey("Bucket", on_delete=models.CASCADE)
    company = models.ForeignKey("Company", on_delete=models.CASCADE)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        '''return a string representation of this relationship'''
        return f'{self.bucket.bucket_name} includes {self.company.company_name}'

class Investment(models.Model):
    '''encapsulates the idea of an investment of a bucket'''
    # data attributes of an investment 
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)
    bucket = models.ForeignKey("Bucket", on_delete=models.CASCADE)
    shares_owned = models.IntegerField(blank=False)
    purchase_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''returns a string representation of the investment'''
        return f'Purchased on {self.purchase_date}'
    
    def sell(self):
        '''sell an investment etf'''
        print(f'calling sell')
        bucket_price = self.bucket.price_per_share
        shares = Decimal(str(self.shares_owned))
        total_value = shares * bucket_price
        customer = Customer.objects.get(pk=self.customer.pk)
        customer.cash_value += total_value
        customer.stock_value -= total_value
        customer.save()
        return total_value


class InvestmentCompany(models.Model):
    '''encapsulates the idea of an investment of a company'''
    #data attributes of an investment company
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)
    company = models.ForeignKey("Company", on_delete=models.CASCADE)
    shares_purchased = models.IntegerField(blank=False)
    purchase_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''returns a string representation of the investment'''
        return f'Purchased on {self.purchase_date}'
    
    def sell(self):
        '''sell an investment company'''
        self.company.update_stock_price()
        print(f'calling sell')
        stock_price = self.company.stock_price
        shares = Decimal(str(self.shares_purchased))
        total_value = shares * Decimal(str(stock_price))
        customer = Customer.objects.get(pk=self.customer.pk)
        customer.cash_value += total_value
        customer.stock_value -= total_value
        customer.save()
        return total_value

def load_data():
        '''function to load the data records from the nyse csv file into company instances'''
        
        filename = '/Users/khan/Desktop/django/nysetop100.csv'
        f = open(filename)
        f.readline() #discard headers 
        Company.objects.all().delete()

        for line in f:
            fields = line.split(',')

            try: 
                price = Decimal(fields[1].replace(',', '').strip())
                market_cap_str = fields[3].strip().upper().replace(',', '')
                if market_cap_str.endswith('B'):
                    market_cap = Decimal(market_cap_str[:-1]) * 1_000_000_000
                elif market_cap_str.endswith('M'):
                    market_cap = Decimal(market_cap_str[:-1]) * 1_000_000
                else:
                    market_cap = Decimal(market_cap_str)
                company = Company(company_name=fields[0],
                                  stock_symbol=fields[4],
                                  market_cap=market_cap,
                                  industry=fields[5],
                                  stock_price=price,
                )
                company.save()
            except: 
                print(f"Skipped: {fields}")