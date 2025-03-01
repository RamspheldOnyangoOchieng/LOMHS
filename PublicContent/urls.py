from django.urls import path
from . import views
from .views import mpesa_simulate_payment


urlpatterns = [
    path('', views.home, name='home'),
    path('tafiti/', views.tafiti, name='tafiti'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('donations/', views.donations, name='donations'),
    path('volunteer/', views.volunteer, name='volunteer'),
    path('contact/', views.contact, name='contact'),
    path('volunteer_submit/', views.volunteer_submit, name='volunteer_submit'),
    path('news/',views.news,name='news'),
    path('service-request/', views.service_request, name='service_request'),
    path('donate/once/', views.one_time_donation_form, name='one_time_donation_form'),
    path('donate/recurring/', views.recurring_donation_form, name='recurring_donation_form'),
    path('mpesa/simulate/', mpesa_simulate_payment, name='mpesa_simulate_payment'),
    
    
]