from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib import messages

from transaction import emailsend

def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('account:admin_dashboard')
        else:
            return redirect('customer:customer_dashboard')
    context = {}
    return render(request, 'frontend/new/index.html', context)


def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('form_name')
        email = request.POST.get('form_email')
        phone = request.POST.get('form_phone')
        subject = request.POST.get('form_subject')
        message = request.POST.get('form_message')

        final_message = render_to_string('emails/customer_care_email.html', 
        {
            'name': name,
            'email': email,
            'message': message,
            'subject': subject,
            'phone': phone
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
            return redirect('frontend:contact_us')

    context = {}
    return render(request, 'frontend/contact_us.html', context)


def location(request):
    return render(request, 'frontend2/location.html')


def about_us(request):
    return render(request, 'frontend/about_us.html')


import time

def loan_home(request):

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        if full_name:
            time.sleep(4) #delay for 4 seconds
            messages.success(request, 'Your request is submitted successfully, we will get back to you as soon as possible.')
            return redirect('frontend:loan_home')
        else:
            time.sleep(4)
            messages.error(request, 'Your request failed, please try again.')
            return redirect('frontend:loan_home')
    return render(request, 'frontend2/loan_home.html')
