from django.urls import path

from . import views

app_name = 'transaction'
urlpatterns = [
    path("deposit/", views.DepositMoneyView.as_view(), name="deposit_money"),
    path("withdraw/", views.WithdrawMoneyView.as_view(), name="withdraw_money"),
    path("account/transfer/", views.CustomerWithdrawMoneyView.as_view(), name="customer_transfer"),
    path("account/international-transfer/", views.InternationaTransferView.as_view(), name="intern_transfer"),
    path('verify/', views.transactionVerify, name='verify'),

    path('pending/', views.transactionPending, name='pending'),
    path('failed/', views.transactionFailed, name='failed'),
    path('completed/', views.transactionComplete, name='complete'),

    # crud
    path('approve/<str:pk>/', views.approveTransaction, name='approve'),
    path('decline/<str:pk>/', views.declineTransaction, name='decline'),
    path('delete_transaction/<str:pk>/', views.deleteTransaction, name='delete_trans'),

    path("select_transafer_type/", views.select_transafer_type, name="select_transafer_type"),
]