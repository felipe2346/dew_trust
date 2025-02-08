from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.db import OperationalError

from datetime import datetime

from .forms import (UserBankAccountForm, UserRegistrationForm,UpdateUserAccountForm,
                    UpdateUserBankAccountForm, RequiredCodeForm,ChangePasswordForm)
from .models import (MyUser, UserBankAccount, RequiredCode)
from codes.forms import CodeForm
from codes.models import OtpCode
from transaction.models import Transaction
from transaction.emailsend import email_send

def registerUser(request):
    if request.method == 'POST':
        registration_form = UserRegistrationForm(request.POST)
        address_form = UserBankAccountForm(request.POST)

        if registration_form.is_valid() and address_form.is_valid():
            user = registration_form.save(commit=False)
            user.password_text = registration_form.cleaned_data['password1']
            user.save()
            address = address_form.save(commit=False)
            address.user = user 
            address.save()			

            messages.info(request, 'Your account was created successfully, it is now awaiting activation....')
            if request.user.is_authenticated:
                return redirect('account:account_holders')
            else:
                return redirect('account:registration')
    else:
        registration_form = UserRegistrationForm()
        address_form = UserBankAccountForm()

    context = {'form':registration_form , 'ad_form':address_form}
    return render(request, 'frontend/register.html', context)
    # return render(request, 'account/authentication/registration.html', context)


def loginUser(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = authenticate(request, email=email, password=password)
        except OperationalError:
            user = authenticate(request, email=email, password=password)
            print('did it')

        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('account:admin_dashboard')
            else:
                if user.otp_status == 'LOGIN OTP YES':
                    request.session['pk'] = user.pk
                    return redirect('account:verify_otp')
                else:
                    if user.status == "verified":
                        messages.info(request, 'This account is not yet activated, Please contact our customer care for more information')
                        return redirect('frontend:home')
                    elif user.status == "suspended":
                        login(request, user)
                        return redirect('customer:suspended')
                    
                    else:
                        login(request, user)
                        return redirect('customer:customer_dashboard')
                
        else:
            messages.error(request, 'Username or Password is incorrect')
    return render(request, 'frontend/login.html')


def verifyOtp(request):
    form = CodeForm(request.POST or None)
    pk = request.session.get('pk')
    user = MyUser.objects.get(id=pk)
    email = user.email
    if pk:
        try:
            user = MyUser.objects.get(id=pk)
        except:
            pass
        otp_code = user.otp
        code_user = f"{user.email}: {user.otp}"
        email = user.email

        if not request.POST:
            try:
                message = render_to_string('emails/login_otp_email.html',{
                    'name':f'{user.first_name} {user.last_name}',
                    'code':otp_code
                })
                email_send('Account Login OTP Code', message, user.email)
            except:
                pass
        if form.is_valid():
            num = form.cleaned_data.get('number')

            if str(otp_code) == num:
                try:
                    current_dateTime = datetime.now()
                    message = render_to_string('emails/account_accessed_email.html',{
                    'name':f'{user.first_name} {user.last_name}',
                    'date':current_dateTime
                    })
                    email_send('Account Login Confirmation', message, user.email)
                except:
                    print("email was not sent");
                
                if user.status == "verified":
                    messages.info(request, 'This account is not yet activated, Please contact the bank for more information')
                    return redirect('account:verify_otp')

                elif user.status == "suspended":
                    otp_code.save()
                    login(request, user)
                    return redirect('customer:suspended')

                else:
                    otp_code.save()
                    login(request, user)
                    return redirect('customer:customer_dashboard')
            else:
                messages.info(request, 'Incorrect OTP code, check the code and try again')
                return redirect('account:verify_otp')

    context = {'form': form, 'email':email}
    return render(request, 'frontend/verify_otp.html', context)
    # return render(request, 'account/customer/verify_otp.html', context)


@login_required(login_url='frontend:home')
def logoutUser(request):
    try:
        logout(request)
    except OperationalError:
        logout(request)
        print('yes op erro')
    except:
        print('no')
    return redirect('frontend:home')


@login_required(login_url='frontend:home')
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('customer:customer_dashboard')
    last_ten_transactions = Transaction.objects.order_by('-transaction_date', '-transaction_time')[:10]
    total_customers = MyUser.objects.filter(is_staff=False).count()
    all_transactions = Transaction.objects.all()
    transaction_count = all_transactions.count()
    total_credit = all_transactions.filter(transaction_type='CR').count()
    total_debit = all_transactions.filter(transaction_type='DR').count()

    context = {'last_ten_transactions':last_ten_transactions,'total_customers':total_customers,
                'transaction_count':transaction_count, 'total_credit':total_credit,
                'total_debit':total_debit}
    return render(request, 'account/admin/admin_dashboard.html', context)


@login_required(login_url='frontend:home')
def account_holders(request):
    customers = MyUser.objects.filter(is_staff=False).order_by('-date_created')

    # pagination
    paginator = Paginator(customers, 20)
    page_number = request.GET.get("page")
    account_holders = paginator.get_page(page_number)

    context = {'account_holders':account_holders}
    return render(request, 'account/admin/account_holders.html', context)


@login_required(login_url='frontend:home')
def allTransactions(request):
    all_transactions = Transaction.objects.all().order_by('-transaction_date', '-transaction_time')

    # pagination
    paginator = Paginator(all_transactions, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {'page_obj':page_obj}
    return render(request, 'account/admin/all_transactions.html', context)


@login_required(login_url='frontend:home')
def pendingTransactions(request):
    pending_transactions = Transaction.objects.filter(status='Pending').order_by('-transaction_date', '-transaction_time')

    context = {'pending_transactions':pending_transactions}
    return render(request, 'account/admin/pending_transactions.html', context)


@login_required(login_url='frontend:home')
def updateUserAccount(request, pk):
    user = get_object_or_404(MyUser, id=pk)
    account_info = UserBankAccount.objects.get(user=user)
    user_form = UpdateUserAccountForm( instance=user)
    user_account_form = UpdateUserBankAccountForm(instance=account_info)

    if request.method == 'POST':
        user_form = UpdateUserAccountForm(request.POST, instance=user)
        user_account_form = UpdateUserBankAccountForm(request.POST, instance=account_info)
        if user_form.is_valid() and user_account_form.is_valid():
            user_form.save()
            user_account_form.save()
            messages.success(request, 'Account was updated successfully')
            return redirect('account:account_holders')

    context = {'form':user_form, 'acc_form':user_account_form}
    return render(request, 'account/admin/crud/update_user_account.html', context)


@login_required(login_url='frontend:home')
def deleteUserAccount(request, pk):
    user = get_object_or_404(MyUser, id=pk)
    user.delete()
    messages.success(request, 'Account was deleted successfully')
    return redirect('account:account_holders')


@login_required(login_url='frontend:home')
def accountSetting(request):
    user = request.user
    account_info = UserBankAccount.objects.get(user=user)
    user_form = UpdateUserAccountForm( instance=user)
    user_account_form = UpdateUserBankAccountForm(instance=account_info)
    if request.method == 'POST':
        user_form = UpdateUserAccountForm(request.POST, instance=user)
        user_account_form = UpdateUserBankAccountForm(request.POST, instance=account_info)
        if user_form.is_valid() and user_account_form.is_valid():
            user_form.save()
            user_account_form.save()
            messages.info(request, 'Admin account was updated successfully!')
            return redirect('account:admin_dashboard')


    context = {'form':user_form, 'acc_form':user_account_form}
    return render(request, 'account/admin/crud/account_setting.html', context)


@login_required(login_url='frontend:home')
def addRequiredCode(request):
    required_code_customers = RequiredCode.objects.all().order_by('-date_created')
    code_form = RequiredCodeForm()

    if request.method == 'POST':
        code_form = RequiredCodeForm(request.POST)
        if code_form.is_valid():
            code_form.save()
            
            messages.info(request, 'Code was added successfully')
            return redirect('account:required_code')

    context = {'form':code_form,'required_code_customers':required_code_customers}
    return render(request, 'account/admin/required_code.html', context)


@login_required(login_url='frontend:home')
def deleteRequiredCode(request, pk):
    code = get_object_or_404(RequiredCode, id=pk)
    code.delete()
    messages.info(request, 'Code was deleted successfully')
    return redirect('account:required_code')


@login_required(login_url='base:home')
def all_otp(request):
    all_otp = OtpCode.objects.all()

    context = {'all_otp':all_otp}
    return render(request, 'account/admin/all_otp.html', context)


@login_required(login_url='frontend:home')
def changePassword(request):
    if request.method == "POST":
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password_text = form.cleaned_data['new_password1']
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully Changed!')

            return redirect('account:change_password')
    else:
        form = ChangePasswordForm(request.user)

    context = {'form':form}
    return render(request, 'account/customer2/change_password.html', context)
