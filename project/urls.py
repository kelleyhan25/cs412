# File name: urls.py 
# Author: kelley han kelhan@bu.edu 
# Description: all the url to view mappings 


from django.urls import path 
from . import views 
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path(r'', views.HomePageView.as_view(), name="home"),
    path(r'browse/', views.BrowseETFsView.as_view(), name="browse"),
    path(r'companies/', views.CompaniesListView.as_view(), name='companies'),
    path(r'login/', auth_views.LoginView.as_view(template_name='project/login.html'), name="login"),
    path(r'logout/', auth_views.LogoutView.as_view(next_page='home'), name="logout"),
    path(r'account/', views.AccountDetailView.as_view(), name="account"),
    path(r'my_investments/', views.MyInvestmentsDetailView.as_view(), name="my_investments"),
    path(r'company/<int:pk>', views.CompanyDetailView.as_view(), name="company_detail"),
    path(r'buy_shares/<int:pk>', views.BuyETFShares.as_view(), name="buy_shares"),
    path(r'register/', RegistrationView.as_view(), name="register"),
    path(r'sell_etf/<int:pk>', SellETFShares.as_view(), name="sell_etf"),
    path(r'sell_company/<int:pk>', SellCompanyShares.as_view(), name="sell_company"),
    path(r'insufficient_funds/', InsufficientFundsView.as_view(), name="insufficient_funds"),
]