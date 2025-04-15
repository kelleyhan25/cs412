# File: models.py 
# Author : Kelley Han kelhan@bu.edu 4/13/25
# Description: All of the models necessary for the ETF Manager project 
from django.db import models

# Create your models here.
class Customer(models.Model):
    '''encapsulates the idea of a customer and its attributes'''

    # data attributes of a Customer 
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    email = models.EmailField(blank=False)
    dob = models.DateField(blank=False)
    account_balance = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        '''return a string representation of this Customer object'''
        return f'{self.first_name} {self.last_name}'

class Company(models.Model):
    '''encapsulates the idea of a company and its attributes'''

    #data attributes of a company 
    company_name = models.TextField(blank=False)
    stock_symbol = models.CharField(max_length=4)
    market_cap = models.DecimalField(max_digits=10, decimal_places=2)
    industry = models.TextField(blank=False)
    stock_price = models.DecimalField(max_digits=10, decimal_places=2)

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
    

    def __str__(self):
        '''return a string representation of this Bucket'''
        return f'{self.bucket_name}'

class BucketCompany(models.Model):
    '''encapsulates the relationship (many to many) with bucket and companies.'''
    bucket = models.ForeignKey("Bucket", on_delete=models.CASCADE)
    company = models.ForeignKey("Company", on_delete=models.CASCADE)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        '''return a string representation of this relationship'''
        return f'{self.bucket.bucket_name} includes {self.company.company_name}'

class Investment(models.Model):
    '''encapsulates the idea of an investment'''
    # data attributes of an investment 
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)
    bucket = models.ForeignKey("Bucket", on_delete=models.CASCADE)
    shares_owned = models.IntegerField(blank=False)
    purchase_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''returns a string representation of the investment'''
        return f'Purchased on {self.purchase_date}'