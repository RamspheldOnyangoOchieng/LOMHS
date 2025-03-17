from django.db import models

class Service(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.CharField(max_length=100, help_text="Bootstrap icon class (e.g., 'bi-hospital')")
    
    def __str__(self):
        return self.title

class Impact(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.CharField(max_length=100, help_text="FontAwesome/Bootstrap icon class (e.g., 'bi-tree')")
    color = models.CharField(max_length=20, default="primary", help_text="Bootstrap color class (e.g., 'text-success')")

    def __str__(self):
        return self.title

class Donation(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    donor_name = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.donor_name} - {self.amount}"

class RecurringDonation(models.Model):
    PAYMENT_METHODS = [
        ('mpesa', 'M-Pesa'),
        ('paypal', 'PayPal'),
        ('card', 'Credit/Debit Card')
    ]
    FREQUENCIES = [
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly')
    ]

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    frequency = models.CharField(max_length=10, choices=FREQUENCIES, default='monthly')
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    mpesa_number = models.CharField(max_length=15, blank=True, null=True)
    paypal_email = models.EmailField(blank=True, null=True)
    card_number = models.CharField(max_length=16, blank=True, null=True)
    expiry_date = models.CharField(max_length=7, blank=True, null=True)
    cvv = models.CharField(max_length=4, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} ({self.frequency}) via {self.payment_method}"


class PayPalTransaction(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]

    donation = models.ForeignKey('Donation', on_delete=models.CASCADE, related_name='paypal_transactions')
    paypal_order_id = models.CharField(max_length=255, unique=True)
    paypal_payment_id = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_details = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"PayPal Transaction {self.paypal_order_id} - {self.status}"

    class Meta:
        ordering = ['-created_at']
