from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('hospital', 'Hospital'),
        ('bloodbank', 'Blood Bank'),
        ('donor', 'Donor'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=100, blank=True)
    blood_group = models.CharField(max_length=5, blank=True)

class BloodRequest(models.Model):
    URGENCY_CHOICES = (
        ('critical', 'Critical'),
        ('moderate', 'Moderate'),
        ('low', 'Low'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('matched', 'Matched'),
        ('fulfilled', 'Fulfilled'),
    )
    hospital = models.ForeignKey(User, on_delete=models.CASCADE)
    blood_type = models.CharField(max_length=5)
    units_needed = models.IntegerField()
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

class Inventory(models.Model):
    blood_bank = models.ForeignKey(User, on_delete=models.CASCADE)
    blood_type = models.CharField(max_length=5)
    units_available = models.IntegerField()
    expiry_date = models.DateField()
# Create your models here.
