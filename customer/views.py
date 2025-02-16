import math
from datetime import datetime

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models.functions import ExtractMonth
from django.db.models import Avg
from django.core.paginator import Paginator
from django.template.loader import render_to_string

from transaction.models import Transaction
from account.models import UserBankAccount
from account.forms import UpdateCustomerAccountForm, UpdateProfilePictureForm
from transaction import emailsend



@login_required(login_url='frontend:home')
def customer_dashboard(request):
    if request.user.status == 'suspended':
        return redirect('customer:suspended')

    user = request.user.account
    ledger_balance = user.balance - 1500

    all_transactions = Transaction.objects.filter(account=user)
    credit_transactions = all_transactions.filter(transaction_type='CR')
    debit_transactions = all_transactions.filter(transaction_type='DR')

    graph_trans = all_transactions.annotate(month=ExtractMonth("transaction_date")).values("month").annotate(sum=Avg("balance_after_transaction")).values('month', 'sum')	
    month_of_year = []
    total_transaction = []
    for i in graph_trans:
        k = str(i['month'])
        k = datetime.strptime(k,'%m')
        k = k.strftime('%B')
        y = i['sum']
        month_of_year.append(k)
        total_transaction.append(y)
    

    all_count = all_transactions.count()
    credit_count = credit_transactions .count()
    debit_count = debit_transactions.count()

    sum_all_transactions = sum(item.amount   for item in all_transactions)
    all_credit = sum(item.amount   for item in credit_transactions)
    all_debit = sum(item.amount   for item in debit_transactions)

    debit_percent = math.ceil((debit_count * 100) / all_count) if debit_count !=0 and all_count !=0 else 0
    credit_percent = math.floor((credit_count * 100) / all_count) if credit_count !=0 and all_count !=0 else 0
    gross_credit_percent = math.ceil((all_credit * 100) / sum_all_transactions) if all_credit !=0 and sum_all_transactions !=0 else 0
    gross_debit_percent = math.floor((all_debit * 100) / sum_all_transactions) if all_debit !=0 and sum_all_transactions !=0 else 0

    user_ip_address = request.META.get('REMOTE_ADDR')

    context = {'credit_count':credit_count,'debit_count':debit_count,
            'credit_percent':credit_percent,'debit_percent':debit_percent,
            'gross_debit_percent':gross_debit_percent,'gross_credit_percent':gross_credit_percent,
            'ledger_balance':ledger_balance, 'month':month_of_year, 'sum':total_transaction, 'ip':user_ip_address, 'all_debit':all_debit}
    
    return render(request, 'account/customer2/customer_dashboard.html', context)


@login_required(login_url='frontend:home')
def userAccountStatement(request):
    if request.user.status == 'suspended':
        return redirect('customer:customer_dashboard')

    user = request.user
    user_account = user.account
    all_transactions = Transaction.objects.filter(account=user_account)

    paginator = Paginator(all_transactions, 25)  

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {'page_obj':page_obj}
    return render(request, 'account/customer2/user_account_statement.html', context)


@login_required(login_url='frontend:home')
def notification(request):
    if request.user.status == 'suspended':
        return redirect('customer:customer_dashboard')
    
    user = request.user
    user_account = user.account
    notifications = Transaction.objects.filter(account=user_account)


    context = {'notifications':notifications, 'user_account':user_account}
    return render(request, 'account/customer/notification.html', context)


@login_required(login_url='frontend:home')
def customer_care(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        final_message = render_to_string('emails/customer_care_email.html', 
        {
            'name': name,
            'email': email,
            'message': message,
            'subject': subject
        })
        try:
            emailsend.email_send(
                'Email From '+name,
                final_message,
                'contact@pinnacleonlinetb.com',
            )
            messages.success(request, 'Email sent successfully, we will get back to you as soon as possible')
        except:
            messages.error(request, 'There was an error while trying to send your email, please try again')

        finally:
            return redirect('customer:customer_care')
    return render(request, 'account/customer2/customer_care.html')


@login_required(login_url='frontend:home')
def loan(request):
    return render(request, 'account/customer2/loan.html')


@login_required(login_url='frontend:home')
def customerAccountSetting(request):
    user = request.user
    user_form = UpdateCustomerAccountForm(instance=user)
    if request.method == 'POST':
        user_form = UpdateCustomerAccountForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
            
            messages.info(request, 'Your account was updated successfully!')
            return redirect('customer:customer_account_setting')

    context = {'form':user_form}
    return render(request, 'account/customer2/customer_account_setting.html', context)


@login_required(login_url='frontend:home')
def updateProfile(request):
    form = UpdateProfilePictureForm(instance=request.user.profile)

    if request.method == 'POST':
        form = UpdateProfilePictureForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile picture was uploaded successfully')
            return redirect('customer:update_profile')

    context = {'form':form}
    return render(request, 'account/customer2/update_profile.html', context)


@login_required(login_url='frontend:home')
def userMoreDetails(request):
    user = request.user
    account_info = UserBankAccount.objects.get(user=user)

    context = {'account_info':account_info,'user':user}
    return render(request, 'account/customer/more_details.html', context)


@login_required(login_url='base:home')
def customerSuspended(request):
    if request.user.status != 'suspended':
        return redirect('customer:customer_dashboard')

    user = request.user.account
    ledger_balance = user.balance - 1500

    all_transactions = Transaction.objects.filter(account=user)
    credit_transactions = all_transactions.filter(transaction_type='CR')
    debit_transactions = all_transactions.filter(transaction_type='DR')

    graph_trans = all_transactions.annotate(month=ExtractMonth("transaction_date")).values("month").annotate(sum=Avg("balance_after_transaction")).values('month', 'sum')	
    month_of_year = []
    total_transaction = []
    for i in graph_trans:
        k = str(i['month'])
        k = datetime.strptime(k,'%m')
        k = k.strftime('%B')
        y = i['sum']
        month_of_year.append(k)
        total_transaction.append(y)
    

    all_count = all_transactions.count()
    credit_count = credit_transactions .count()
    debit_count = debit_transactions.count()

    sum_all_transactions = sum(item.amount   for item in all_transactions)
    all_credit = sum(item.amount   for item in credit_transactions)
    all_debit = sum(item.amount   for item in debit_transactions)

    debit_percent = math.ceil((debit_count * 100) / all_count) if debit_count !=0 and all_count !=0 else 0
    credit_percent = math.floor((credit_count * 100) / all_count) if credit_count !=0 and all_count !=0 else 0
    gross_credit_percent = math.ceil((all_credit * 100) / sum_all_transactions) if all_credit !=0 and sum_all_transactions !=0 else 0
    gross_debit_percent = math.floor((all_debit * 100) / sum_all_transactions) if all_debit !=0 and sum_all_transactions !=0 else 0

    context = {'credit_count':credit_count,'debit_count':debit_count,
            'credit_percent':credit_percent,'debit_percent':debit_percent,
            'gross_debit_percent':gross_debit_percent,'gross_credit_percent':gross_credit_percent,
            'ledger_balance':ledger_balance, 'month':month_of_year, 'sum':total_transaction}
    
    return render(request, 'account/customer2/suspended.html', context)
