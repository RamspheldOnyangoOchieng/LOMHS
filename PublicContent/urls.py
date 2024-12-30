from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tafiti/', views.tafiti, name='tafiti'),
    path('donations/', views.donations, name='donations'),
    path('volunteer/', views.volunteer, name='volunteer'),
]