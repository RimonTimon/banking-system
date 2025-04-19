
from django.db import models
from django.contrib.auth.models import User
import random

ACCOUNT_TYPES = [
    ('savings', 'Savings'),
    ('current', 'Current'),
    ('fixed', 'Fixed Deposit'),
    ('student', 'Student'),
    ('joint', 'Joint Account'),
]

GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
]

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    nationality = models.CharField(max_length=50)
    nid_passport = models.CharField(max_length=50)
    present_address = models.TextField()
    permanent_address = models.TextField()
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    account_number = models.CharField(max_length=12, unique=True, editable=False)
    balance = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=5000.00
    )
    currency = models.CharField(max_length=10, default='USD')
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = self.generate_account_number()
        super().save(*args, **kwargs)

    def generate_account_number(self):
        return "10" + str(random.randint(1000000000, 9999999999))

    def __str__(self):
        return f"{self.full_name} - {self.account_number}"
    


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
    )
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True, null=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
    
    
class FixedDeposit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    tenure_months = models.IntegerField(default=12)
    interest_rate = models.FloatField(default=7.5)  # in percentage
    created_at = models.DateTimeField(auto_now_add=True)
    maturity_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)