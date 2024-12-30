from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html')

def tafiti(request):
    return render(request, 'tafiti.html')

def donations(request):
    return render(request, 'donations.html')

def volunteer(request):
    return render(request, 'volunteer.html')