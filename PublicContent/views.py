from django.shortcuts import render
from django.templatetags.static import static
from .models import Service, Impact  # Import your models

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
        # Process form data & handle payment
        return redirect('donation_success')  # or wherever you'd like
    return render(request, 'one_time_donation_form.html')

def recurring_donation_form(request):
    if request.method == 'POST':
        # Process form data & handle payment
        return redirect('donation_success')
    return render(request, 'recurring_donation_form.html')



from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt


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

