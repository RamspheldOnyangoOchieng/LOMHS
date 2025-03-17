"""
from django import forms
from .models import RecurringDonation

class RecurringDonationForm(forms.ModelForm):
    class Meta:
        model = RecurringDonation
        fields = [
            'monthly_amount', 'first_name', 'last_name', 'email', 'phone',
            'address_line1', 'address_line2', 'city', 'state', 'zip_code', 'country',
            'payment_method', 'card_name', 'card_number', 'expiry_month', 'expiry_year', 'cvv'
        ]
        widgets = {
            'payment_method': forms.Select(attrs={'class': 'form-control', 'onchange': 'updatePaymentMethodRecurring()'}),
            # You can add additional widget customizations here
        }

PAYPAL_CLIENT_ID = 'your_client_id'
PAYPAL_CLIENT_SECRET = 'your_client_secret'
PAYPAL_MODE = 'sandbox'  # or 'live' for production

"""

from django import forms
from .models import RecurringDonation

class RecurringDonationForm(forms.ModelForm):
    class Meta:
        model = RecurringDonation
        fields = [
            'amount',
            'frequency',
            'payment_method',
            'mpesa_number',
            'paypal_email',
            'card_number',
            'expiry_date',
            'cvv',
        ]
