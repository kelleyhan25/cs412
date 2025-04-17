from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Customer)
admin.site.register(Company)
admin.site.register(Bucket)
admin.site.register(Investment)
admin.site.register(BucketCompany)
admin.site.register(InvestmentCompany)