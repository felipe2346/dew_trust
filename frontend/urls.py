from django.urls import path

from . import views

app_name = 'frontend'
urlpatterns = [
    path('', views.home, name='home'),
    path('contact-us-now/', views.contact_us, name='contact_us'),
    path('location/', views.location, name='location'),
    path('about_us/', views.about_us, name='about_us'),
    path('apply/loan/', views.loan_home, name='loan_home'),
]