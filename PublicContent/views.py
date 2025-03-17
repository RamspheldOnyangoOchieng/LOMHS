from django.templatetags.static import static
from .models import Service, Impact, Donation, PayPalTransaction, RecurringDonation
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RecurringDonationForm
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.urls import reverse
import json
import uuid
from django.conf import settings
import requests

# Basic Page Views
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

def contact(request):
    return render(request, 'contact.html')

def volunteer_submit(request):
    return render(request, 'volunteer_submit.html')

def news(request):
    return render(request, 'news.html')

def services(request):
    # List of static images
    image_list = [
        "farm.jpeg", "farm1.jpeg", "green1.jpeg", "green2.jpeg",
        "image.png", "h1.jpeg", "images.jpeg"
    ]
    images = [static(f"images/{img}") for img in image_list]  # Prepend static path

    # Define services dynamically
    services = [
        {"title": "Healthcare Access", "description": "Providing affordable healthcare to underserved communities.", "icon": "bi-heart"},
        {"title": "Environmental Conservation", "description": "Promoting sustainable practices and green solutions.", "icon": "bi-tree"},
        {"title": "Education & Training", "description": "Empowering individuals through education and skill development.", "icon": "bi-book"},
        {"title": "Community Support", "description": "Creating support networks for mental health and well-being.", "icon": "bi-people"},
    ]

    # Define impact highlights
    impacts = [
        {"title": "10,000+ Lives Impacted", "description": "Through our healthcare and support programs.", "icon": "bi-people-fill", "color": "primary"},
        {"title": "500+ Trees Planted", "description": "As part of our environmental sustainability efforts.", "icon": "bi-tree-fill", "color": "success"},
        {"title": "100+ Scholarships Awarded", "description": "Supporting students with access to quality education.", "icon": "bi-award-fill", "color": "warning"},
    ]

    context = {
        "images": images,
        "services": services,
        "impacts": impacts
    }
    return render(request, "services.html", context)

def service_request(request):
    return render(request, "service_request.html")

def one_time_donation_form(request):
    if request.method == 'POST':
        # Process one-time donation form data and handle payment
        return redirect('donation_success')
    return render(request, 'one_time_donation_form.html')

def recurring_donation_form(request):
    if request.method == 'POST':
        form = RecurringDonationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for setting up your recurring donation!")
            return redirect('recurring_donation_success')
    else:
        form = RecurringDonationForm()
    return render(request, 'recurring_donation_form.html', {'form': form})

# Mpesa Payment Functions
MPESA_CONSUMER_KEY = "BilJfQ6hQ84LOlTllFTMGZAFcRGKOCMmnqgGOqWA561AfxyM"
MPESA_CONSUMER_SECRET = "3pyoY3xR86oS7CpRXG9dSt7SVqnAzidBkqZRpBMiZB4J9wvcSj5zA17DTtRA6emt"
MPESA_SHORTCODE = "600000" 
MPESA_COMMAND_ID = "CustomerPayBillOnline"  
MPESA_BILL_REF = "Donation"  
MPESA_API_BASE = "https://sandbox.safaricom.co.ke"

def get_mpesa_access_token():
    """
    Generates an Mpesa access token using the Daraja API.
    """
    auth_url = f"{MPESA_API_BASE}/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(auth_url, auth=(MPESA_CONSUMER_KEY, MPESA_CONSUMER_SECRET))
    token_data = response.json()
    return token_data.get("access_token", None)

@csrf_exempt  
def mpesa_simulate_payment(request):
    """
    Simulates a C2B Mpesa payment by posting to the Daraja API.
    Expects POST data containing 'phone' and 'amount'.
    """
    if request.method == "POST":
        phone_number = request.POST.get("phone")
        amount = request.POST.get("amount")
        if not phone_number or not amount:
            return JsonResponse({"error": "Missing phone number or amount"}, status=400)

        access_token = get_mpesa_access_token()
        if not access_token:
            return JsonResponse({"error": "Could not generate access token"}, status=500)

        simulate_url = f"{MPESA_API_BASE}/mpesa/c2b/v1/simulate"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        payload = {
            "ShortCode": MPESA_SHORTCODE,
            "CommandID": MPESA_COMMAND_ID,
            "Amount": amount,
            "Msisdn": phone_number,       
            "BillRefNumber": MPESA_BILL_REF,
        }
        response = requests.post(simulate_url, json=payload, headers=headers)
        return JsonResponse(response.json())
    else:
        return HttpResponse("Method not allowed", status=405)

# PayPal Payment Functions
def initiate_paypal_payment(request, donation_id):
    try:
        donation = Donation.objects.get(id=donation_id)
        
        # Generate a unique order ID
        order_id = str(uuid.uuid4())
        
        # Create PayPal transaction record
        transaction = PayPalTransaction.objects.create(
            donation=donation,
            paypal_order_id=order_id,
            # For recurring donations, adjust accordingly:
            amount=donation.monthly_amount if hasattr(donation, "monthly_amount") and donation.is_recurring else donation.amount,
            status='pending'
        )
        
        context = {
            'amount': float(transaction.amount),
            'description': f"Donation to {settings.SITE_NAME}",
            'donation_id': donation_id,
            'recurring': getattr(donation, "is_recurring", False),
            'order_id': order_id
        }
        
        return render(request, 'paypal_payment.html', context)
    except Donation.DoesNotExist:
        return JsonResponse({'error': 'Donation not found'}, status=404)

@csrf_exempt
@require_POST
def process_paypal_payment(request):
    try:
        data = json.loads(request.body)
        order_id = data.get('order_id')
        payment_id = data.get('payment_id')
        status = data.get('status')
        
        transaction = PayPalTransaction.objects.get(paypal_order_id=order_id)
        # Update transaction details
        transaction.paypal_payment_id = payment_id
        transaction.status = status
        transaction.payment_details = data
        transaction.save()
        
        if status == 'completed':
            donation = transaction.donation
            donation.status = 'completed'
            donation.save()
            return JsonResponse({
                'success': True,
                'redirect_url': reverse('donation_success')
            })
        
        return JsonResponse({
            'success': False,
            'error': 'Payment processing failed'
        })
    except PayPalTransaction.DoesNotExist:
        return JsonResponse({'error': 'Transaction not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_POST
def paypal_webhook(request):
    try:
        data = json.loads(request.body)
        event_type = data.get('event_type')
        if event_type == 'PAYMENT.CAPTURE.COMPLETED':
            order_id = data.get('resource', {}).get('custom_id')
            payment_id = data.get('resource', {}).get('id')
            try:
                transaction = PayPalTransaction.objects.get(paypal_order_id=order_id)
                transaction.paypal_payment_id = payment_id
                transaction.status = 'completed'
                transaction.payment_details = data
                transaction.save()
                donation = transaction.donation
                donation.status = 'completed'
                donation.save()
            except PayPalTransaction.DoesNotExist:
                pass
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Process Recurring Donation
def process_recurring_donation(request):
    if request.method == "POST":
        # Extract form data from POST request
        amount = request.POST.get("amount")
        frequency = request.POST.get("frequency")
        payment_method = request.POST.get("payment_method")
        mpesa_number = request.POST.get("mpesa_number") if payment_method == "mpesa" else None
        paypal_email = request.POST.get("paypal_email") if payment_method == "paypal" else None
        card_number = request.POST.get("card_number") if payment_method == "card" else None
        expiry = request.POST.get("expiry") if payment_method == "card" else None
        cvv = request.POST.get("cvv") if payment_method == "card" else None

        # Create a RecurringDonation record
        donation = RecurringDonation.objects.create(
            amount=amount,
            frequency=frequency,
            payment_method=payment_method,
            mpesa_number=mpesa_number,
            paypal_email=paypal_email,
            card_number=card_number,
            expiry_date=expiry,
            cvv=cvv,
        )

        # Route based on the selected payment method
        if payment_method == "mpesa":
            return redirect("mpesa_payment", donation_id=donation.id)
        elif payment_method == "paypal":
            # Create a unique order ID for PayPal
            order_id = str(uuid.uuid4())

            # Build the context for the PayPal payment page
            context = {
                "amount": donation.amount,
                "description": f"Recurring donation to {getattr(settings, 'SITE_NAME', 'My Donation Site')}",
                "donation_id": donation.id,
                "order_id": order_id,
                "recurring": True,
            }

            return render(request, "paypal_payment.html", context)
        elif payment_method == "card":
            return redirect("card_payment", donation_id=donation.id)

    # For GET requests, simply show the recurring donation form
    return render(request, "recurring_donation.html")
