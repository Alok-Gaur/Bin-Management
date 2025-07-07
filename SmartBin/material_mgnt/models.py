from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class MaterialCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)


class Material(models.Model):
    MATERIAL_TYPES = [
        ('SOLID', 'Solid'),
        ('LIQUID', 'Liquid'),
        ('GAS', 'Gas'),
        ('POWDER', 'Powder'),
        ('OTHER', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(MaterialCategory, on_delete=models.SET_NULL, null=True)
    state = models.CharField(max_length=20, choices=MATERIAL_TYPES)
    hazardable = models.BooleanField(default=False)
    recyclable = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now=True)
    
class MaterialListing(models.Model):
    LISTING_TYPE = [
        ('OFFER', 'Available Material'),
        ('REQUEST', 'Material Needed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listing')
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    listing = models.CharField(max_length=10, choices=LISTING_TYPE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20)
    available_from = models.DateField()
    available_until = models.DateField(null=True, blank=True)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_negotiable = models.BooleanField(default=False)
    location = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now=True)
    