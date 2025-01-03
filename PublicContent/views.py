from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html')

def tafiti(request):
    return render(request, 'tafiti.html')

def donations(request):
    return render(request, 'donate.html')

def volunteer(request):
    return render(request, 'volunteer.html')

def about(request):
    return render(request, 'about.html')


def services(request):
    return render(request, 'services.html')


def contact(request):
    return render(request, 'contact.html')