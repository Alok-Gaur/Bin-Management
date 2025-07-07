from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from material_mgnt.models import MaterialListing


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    company_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"
    
class Transaction(models.Model):
    STATUS = [
        ("PENDING", 'Pending'),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    ]
    listing = models.ForeignKey(MaterialListing, on_delete=models.SET_NULL, null=True)
    provider = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='provided_transactions')
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="received_transactions")
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    agreed_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS)
    transaction_date = models.DateTimeField(auto_now_add=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Transaction #{self.id} - {self.listing.material.name}"