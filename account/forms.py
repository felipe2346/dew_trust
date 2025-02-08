from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm

from django.contrib.auth.models import User


from django.db import transaction

from .models import (MyUser, UserBankAccount, RequiredCode, Profile,)

# from .constants import STATUS_CHOICES, GENDER_CHOICE, TRANSFER_CHOICES, CURRENCY_CHOICE, MONEY_CHOICE

class DateInput(forms.DateInput):
	input_type = 'date'


class UserBankAccountForm(forms.ModelForm):

    class Meta:
        model = UserBankAccount
        fields = ['street_address','city','postal_code','country',
                'account_type','currency', 'anual_income','asset_worth',
                'credit_worth',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class UserRegistrationForm(UserCreationForm):
	
    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2',
                'gender', 'birth_date', 'title', 'password_text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password_text'].widget = forms.HiddenInput()
        self.fields['birth_date'].widget = DateInput()

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class UpdateUserAccountForm(forms.ModelForm):

    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'email','gender', 'birth_date', 'title', 
                'password_text', 'status', 'transfer_status', 'otp_status','created_on']
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['birth_date'].widget = DateInput()
        self.fields['created_on'].widget = DateInput()

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class UpdateUserBankAccountForm(forms.ModelForm):

    class Meta:
        model = UserBankAccount
        fields = ['country','account_type','currency',
                    'anual_income','asset_worth',
                'credit_worth',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class RequiredCodeForm(forms.ModelForm):

    class Meta:
        model = RequiredCode
        fields = ['user', 'code_name', 'code_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class ChangePasswordForm(PasswordChangeForm):
    old_password =  forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = MyUser
        fields = ['old_password', 'new_password1', 'new_password2']


class UpdateCustomerAccountForm(forms.ModelForm):

    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'email','gender', 'birth_date', 'title']
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['birth_date'].widget = DateInput()

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class UpdateProfilePictureForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['picture']
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})