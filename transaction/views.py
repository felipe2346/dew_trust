from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from datetime import datetime
from django.db import OperationalError




from django.views.generic import CreateView, ListView

from .models import Transaction
from account.models import UserBankAccount, MyUser
from . import forms, constants
from .emailsend import email_send


class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = 'transactions/transaction_form.html'
    model = Transaction
    title = ''
    success_url = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title
        })

        return context
    

class DepositMoneyView(TransactionCreateMixin):
    form_class = forms.DepositForm
    title = 'Fund Customer Account'
    success_url = reverse_lazy('transaction:deposit_money')

    def get_initial(self):
        initial = {'transaction_type': constants.CREDIT}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        customer_account = form.cleaned_data.get('account')
        if form.is_valid():
            try:
                account = UserBankAccount.objects.get(account_no=customer_account.account_no)
            except OperationalError:
                account = UserBankAccount.objects.get(account_no=customer_account.account_no)
            transaction = form.save(commit=False)
            transaction.balance_after_transaction = account.balance + amount
            # transaction.status = constants.SUCCESSFUL
            transaction.save()
            account.balance += amount
            account.save(
                update_fields=[
                    'balance',
                ]
            )

            messages.success(
                self.request,
                f'{amount}{account.currency} has been deposited successfully to this account'
            )

        return super().form_valid(form)
    

class WithdrawMoneyView(TransactionCreateMixin):
    form_class = forms.WithdrawForm
    title = 'Debit Customer Account'
    success_url = reverse_lazy('transaction:withdraw_money')

    def get_initial(self):
        initial = {'transaction_type': constants.DEBIT}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        customer_account = form.cleaned_data.get('account')
        if form.is_valid():
            account = UserBankAccount.objects.get(account_no=customer_account.account_no)
            transaction = form.save(commit=False)
            transaction.balance_after_transaction = account.balance - amount
            # transaction.status = constants.SUCCESSFUL
            transaction.save()
            account.balance -= amount
            account.save(update_fields=['balance'])

        messages.success(
            self.request,
            f'Successfully withdrawn {amount}{account.currency} from this account'
        )

        return super().form_valid(form)


class CustomerTransactionCreateMixin(LoginRequiredMixin, CreateView):
    
    model = Transaction

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.status == 'suspended':
            return HttpResponseRedirect(reverse_lazy('customer:suspended'))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        try:
            user_code = self.request.user.code
            return reverse_lazy('transaction:verify')
        
        except MyUser.code.RelatedObjectDoesNotExist:
            if self.request.user.transfer_status == 'Pending':
                return reverse_lazy('transaction:pending')
            elif self.request.user.transfer_status == 'Fail':
                return reverse_lazy('transaction:failed')
            else:
                return reverse_lazy('transaction:complete')
        
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account
        })
        return kwargs
    

class CustomerWithdrawMoneyView(CustomerTransactionCreateMixin):
    form_class = forms.CustomerTransactionForm
    template_name = 'transactions/customer_transfer.html'

    def get_initial(self):
        initial = {'transaction_type': constants.DEBIT, 'transaction_date':timezone.now().date(),
                   'transaction_time':timezone.now().time()}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        
        if form.is_valid():
            data = form.save(commit=False)
            try:
                user_code = self.request.user.code
                data.status = constants.FAILED
                data.save()
                try:
                    self.request.session['pk'] = data.pk
                    
                except AttributeError:
                    messages.info(self.request, 'Something went wrong, Please Try again') 
                    return self.render_to_response(self.get_context_data(form=form))
                
            except MyUser.code.RelatedObjectDoesNotExist:
                if self.request.user.transfer_status == 'Pending':
                    data.status = constants.PENDING
                    data.save()
                    self.request.user.account.balance -= amount
                    self.request.user.account.save(update_fields=['balance'])

                    message = render_to_string('emails/transaction_pending_email.html',{
                    'name': self.request.user.get_full_name(),
                    'amount': data.amount,
                    'date': datetime.now(),
                    'currency': data.account.currency,
                    })
                    try:
                        email_send('Transaction Pending', message, self.request.user.email)
                    except:
                        print("Email was not sent due to connection error")
                    
                elif self.request.user.transfer_status == 'Fail':
                    data.status = constants.FAILED
                    data.save()

                    message = render_to_string('emails/transaction_failed_email.html',{
                    'name': self.request.user.get_full_name(),
                    'amount': data.amount,
                    'date': datetime.now(),
                    'currency': data.account.currency,
                    })
                    try:
                        email_send('Transaction Failed', message, self.request.user.email)
                    except:
                        print("Email was not sent due to connection error")

                else:
                    data.status = constants.SUCCESSFUL
                    data.save()
                    self.request.user.account.balance -= amount
                    self.request.user.account.save(update_fields=['balance'])
                    self.request.session['pk'] = data.pk

                    message = render_to_string('emails/transaction_complete_email.html',{
                    'name': self.request.user.get_full_name(),
                    'date': data.date_created,
                    'account_number':str(data.beneficiary_account),
                    'summery': data.description,
                    'amount':f'{data.account.currency}{data.amount}',
                    'balance':f'{data.account.currency}{data.balance_after_transaction}',

                    })
                    try:
                        email_send('Transaction Completed', message, self.request.user.email)
                    except:
                        print("Email was not sent due to connection error")

        return super().form_valid(form)


@login_required(login_url='frontend:home')
def transactionVerify(request):
    if request.user.status == 'suspended':
        return redirect('customer:customer_dashboard')

    required_code = request.user.code
    user_account = request.user.account
    pk = request.session.get('pk')

    if request.method == 'POST':
        transaction_code = request.POST.get('trans-code')	
        if pk:
            transaction = Transaction.objects.get(id=pk)
            if transaction_code == required_code.code_number:
                if request.user.transfer_status == 'Pending':
                    transaction.balance_after_transaction = user_account.balance - transaction.amount
                    transaction.status = 'Pending'
                    transaction.save()
                    user_account.balance = transaction.balance_after_transaction
                    user_account.save()
                    message = render_to_string('emails/transaction_pending_email.html',{
                    'name':f'{request.user.first_name} {request.user.last_name}',
                    'amount': transaction.amount,
                    'date': datetime.now(),
                    'currency': transaction.account.currency,
                    })
                    try:
                        email_send('Transaction Pending', message, request.user.email)
                    except:
                        print("Email was not sent due to connection error")
                    finally:
                        return redirect('transaction:pending')

                elif request.user.transfer_status == 'Fail':
                    transaction.save()
                    message = render_to_string('emails/transaction_failed_email.html',{
                    'name':f'{request.user.first_name} {request.user.last_name}',
                    'amount': transaction.amount,
                    'date': datetime.now(),
                    'currency': transaction.account.currency,
                    })
                    try:
                        pass
                        email_send('Transaction Failed', message, request.user.email)
                    except:
                        print("Email was not sent due to connection error")
                    finally:
                        return redirect('transaction:failed')

                else:
                    transaction.balance_after_transaction = user_account.balance - transaction.amount
                    transaction.status = 'Successful'
                    transaction.save()
                    user_account.balance = transaction.balance_after_transaction
                    user_account.save()

                    message = render_to_string('emails/transaction_complete_email.html',{
                    'name':f'{request.user.first_name} {request.user.last_name}',
                    'date': transaction.date_created,
                    'account_number':str(transaction.beneficiary_account),
                    'summery': transaction.description,
                    'amount':f'{transaction.amount} {transaction.account.currency}',
                    'balance':f'{transaction.balance_after_transaction} {transaction.account.currency}',

                    })
                    try:
                        pass
                        email_send('Transaction Completed', message, request.user.email)
                    except:
                        print("Email was not sent due to connection error")
                    finally:
                        # getting session
                        request.session['pk'] = transaction.pk
                        return redirect('transaction:complete')
            else:
                transaction.status = 'Failed'
                transaction.save()
                messages.info(request, 'The code you entered is incorrect, please check the code and try again')

            
    context = {'required_code': required_code}	
    return render(request, 'transactions/verify.html', context)
    

@login_required(login_url='frontend:home')
def transactionPending(request):
    return render(request, 'transactions/pending.html')


@login_required(login_url='frontend:home')
def transactionFailed(request):
    return render(request, 'transactions/Failed.html')


@login_required(login_url='frontend:home')
def transactionComplete(request):
    transaction = Transaction.objects.filter(account = request.user.account)
    pk = request.session.get('pk')
    current_transaction = transaction.get(pk=pk)
    context = {'transaction': current_transaction}
    return render(request, 'transactions/complete.html', context)



# admin done side

@login_required(login_url='frontend:home')
def approveTransaction(request, pk):
    transaction = Transaction.objects.get(id=pk)
    transaction.status = "Successful"
    transaction.save()
    user = transaction.account.user
    email = user.email
    full_name = user.get_full_name()

    try:
        message = render_to_string('emails/approved.html',{
        'name': full_name,
        'amount': transaction.amount,
        'date': transaction.date_created,
        'currency': transaction.account.currency,

        })
        email_send('Transaction Approved', message, email)
    except:
        pass

    messages.success(request, 'Transaction is approved successfully')
    return redirect('account:pending_transactions')


@login_required(login_url='frontend:home')
def declineTransaction(request, pk):
    transaction = Transaction.objects.get(id=pk)
    amount = transaction.amount
    user_bank_account = UserBankAccount.objects.get(account_no=transaction.account.account_no)

    transaction.status = "Failed"
    transaction.balance_after_transaction += amount
    transaction.save()

    user_bank_account.balance = transaction.balance_after_transaction
    user_bank_account.save()
    email = user_bank_account.user.email

    try:
        message = render_to_string('emails/declined.html',{
        'name':user_bank_account.user.get_full_name(),
        'amount': amount,
        'date': transaction.date_created,
        'currency': transaction.account.currency,

        })
        email_send('Transaction Declined', message, email)
    except:
        pass
    messages.success(request, 'Transaction is declined successfully')
    return redirect('account:pending_transactions')


@login_required(login_url='base:home')
def deleteTransaction(request, pk):
    transaction = Transaction.objects.get(id=pk)
    user_bank_account = UserBankAccount.objects.get(account_no=transaction.account.account_no)
    if transaction.transaction_type == 'DR':
        if transaction.status == 'Failed':
            transaction.delete()
            messages.success(request, 'Transaction is deleted successfully')
            return redirect('account:all_transactions')
        else:
            user_bank_account.balance += transaction.amount
            user_bank_account.save()
            transaction.delete()
            messages.success(request, 'Transaction is deleted successfully')
            return redirect('account:all_transactions')
    else:
        if transaction.status == 'Failed':
            transaction.delete()
            messages.success(request, 'Transaction is deleted successfully')
            return redirect('account:all_transactions')
        else:
            user_bank_account.balance -= transaction.amount
            user_bank_account.save()
            transaction.delete()
            messages.success(request, 'Transaction is deleted successfully')
            return redirect('account:all_transactions')


@login_required(login_url='base:home')
def select_transafer_type(request):
    if request.method == 'POST':
        selected_location = request.POST.get('location')

        if selected_location == 'local':
            return redirect('transaction:customer_transfer')
        elif selected_location == 'international':
            return redirect('transaction:intern_transfer')

        return redirect(reverse('account:customer_dashboard'))
    


class InternationaTransferView(CustomerTransactionCreateMixin):
    form_class = forms.CustomerTransactionForm
    template_name = 'transactions/international_transfer.html'

    def get_initial(self):
        initial = {'transaction_type': constants.DEBIT, 'transaction_date':timezone.now().date(),
                   'transaction_time':timezone.now().time()}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        
        if form.is_valid():
            data = form.save(commit=False)
            try:
                user_code = self.request.user.code
                data.status = constants.FAILED
                data.save()
                try:
                    self.request.session['pk'] = data.pk
                    
                except AttributeError:
                    messages.info(self.request, 'Something went wrong, Please Try again') 
                    return self.render_to_response(self.get_context_data(form=form))
                
            except MyUser.code.RelatedObjectDoesNotExist:
                if self.request.user.transfer_status == 'Pending':
                    data.status = constants.PENDING
                    data.save()
                    self.request.user.account.balance -= amount
                    self.request.user.account.save(update_fields=['balance'])

                    message = render_to_string('emails/transaction_pending_email.html',{
                    'name': self.request.user.get_full_name(),
                    'amount': data.amount,
                    'date': datetime.now(),
                    'currency': data.account.currency,
                    })
                    try:
                        email_send('Transaction Pending', message, self.request.user.email)
                    except:
                        print("Email was not sent due to connection error")
                    
                elif self.request.user.transfer_status == 'Fail':
                    data.status = constants.FAILED
                    data.save()

                    message = render_to_string('emails/transaction_failed_email.html',{
                    'name': self.request.user.get_full_name(),
                    'amount': data.amount,
                    'date': datetime.now(),
                    'currency': data.account.currency,
                    })
                    try:
                        email_send('Transaction Failed', message, self.request.user.email)
                    except:
                        print("Email was not sent due to connection error")

                else:
                    data.status = constants.SUCCESSFUL
                    data.save()
                    self.request.user.account.balance -= amount
                    self.request.user.account.save(update_fields=['balance'])
                    self.request.session['pk'] = data.pk

                    message = render_to_string('emails/transaction_complete_email.html',{
                    'name': self.request.user.get_full_name(),
                    'date': data.date_created,
                    'account_number':str(data.beneficiary_account),
                    'summery': data.description,
                    'amount':f'{data.account.currency}{data.amount}',
                    'balance':f'{data.account.currency}{data.balance_after_transaction}',

                    })
                    try:
                        email_send('Transaction Completed', message, self.request.user.email)
                    except:
                        print("Email was not sent due to connection error")

        return super().form_valid(form)
