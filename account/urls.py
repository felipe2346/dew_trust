from django.urls import path

from . import views

app_name = 'account'
urlpatterns = [

    # authentification
    path('registration/', views.registerUser, name='registration'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('verify_otp/', views.verifyOtp, name='verify_otp'),

    # admin part
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/account_holders/', views.account_holders, name='account_holders'),
    path('admin/all_transactions/', views.allTransactions, name='all_transactions'),
    path('admin/pending_transactions/', views.pendingTransactions, name='pending_transactions'),
    path('admin/required_code/', views.addRequiredCode, name='required_code'),
    path('admin/all_otp/', views.all_otp, name='all_otp'),
    path('change_password/', views.changePassword, name='change_password'),

    # admin crud
    path('admin/update_user/<str:pk>/', views.updateUserAccount, name='update_user'),
    path('admin/delete_user/<str:pk>/', views.deleteUserAccount, name='delete_user'),
    path('admin/account_setting/', views.accountSetting, name='account_setting'),
    path('admin/delete_code/<str:pk>/', views.deleteRequiredCode, name='delete_code'),
]