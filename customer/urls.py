from django.urls import path

from . import views

app_name = 'customer'
urlpatterns = [
    path('customer_dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('account_statement/', views.userAccountStatement, name='user_account_statement'),
    path('account_setting/', views.customerAccountSetting, name='customer_account_setting'),
    path('update_profile/', views.updateProfile, name='update_profile'),
    path('more_details/', views.userMoreDetails, name='more_details'),
    path('suspended/', views.customerSuspended, name='suspended'),
    path('notification/', views.notification, name='notification'),
    path('customer_care/', views.customer_care, name='customer_care'),
    path('loan/', views.loan, name='loan'),
]