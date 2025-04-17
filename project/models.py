# File: models.py 
# Author : Kelley Han kelhan@bu.edu 4/13/25
# Description: All of the models necessary for the ETF Manager project 
from django.db import models
from django.contrib.auth.models import User
import yfinance as yf 
from decimal import Decimal 
from django.utils import timezone 
from datetime import timedelta

def get_stock_price(stock_symbol): 
    '''returns most current stock price'''
    stock =  yf.Ticker(stock_symbol)
    data = stock.history(period="1d")
    if not data.empty: 
        price = float(data['Close'].iloc[-1])
        price = round(price, 2)
        return price
    return None

def get_market_cap(stock_symbol):
    '''returns market cap from yfinance api'''
    stock = yf.Ticker(stock_symbol)
    info = stock.info
    market_cap = info.get('marketCap')
    if market_cap:
        mc = float(market_cap) / 1_000_000_000
        mc = round(mc, 2)
    return None

def get_percent_change(stock_symbol):
    '''returns the percent change of stock price from today and yesterday's closing prices'''
    stock = yf.Ticker(stock_symbol)
    data = stock.history(period="2d")
    if len(data) >=2:
        yesterday = data['Close'].iloc[-2]
        today = data['Close'].iloc[-1]
        percent_change = ((today - yesterday) / yesterday) * 100
        percent_change = round(percent_change, 2)
        return percent_change

def format_price_change(percentage):
    '''adds an up arrow or down arrow based on positive/negative percent change'''
    if percentage is None: 
        return "N/A"
    
    if percentage > 0: 
        return f"↑ {percentage}%"
    elif percentage < 0: 
        return f"↓ {percentage}%"
    else:
        return f"0.00%"


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
        cap = get_market_cap(self.stock_symbol)
        if cap is not None: 
            self.market_cap = Decimal(str(cap))
            self.save()
        return self.market_cap

    def update_stock_price(self):
        '''updates stock price with most recent data from yfinance api'''
        price = get_stock_price(self.stock_symbol)
        if price is not None: 
            self.stock_price = price
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