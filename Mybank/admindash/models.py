from django.db import models
import random
from django.contrib.auth.models import User
from datetime import date
import random
import datetime
# Create your models here.
today = date.today()
try:
    five_years_later = today.replace(year=today.year + 5)
except ValueError:
    five_years_later = today.replace(month=2, day=28, year=today.year + 5)

# User Table
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=100)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    cnic = models.CharField(max_length=30,default='')

    account_number = models.CharField(max_length=20, default='AAA12345678')
    account_type = models.CharField(max_length=20)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=100.00)
    status = models.CharField(max_length=20, default='Inactive')


    def __str__(self):
        return f"{self.user} | {self.first_name} {self.last_name} {self.email}"


# Account Table


# Transaction Table
class Transaction(models.Model):
    trans_id = models.CharField(max_length=25,default='TRX12345678')
    account = models.CharField(max_length=20, default='AAA12345678')
    type = models.CharField(max_length=20 )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)
    recipient_account = models.CharField(max_length=20, default='AAA12345678')
    method = models.CharField(max_length=20, default='')
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.type} - {self.amount} - {self.account} -> {self.recipient_account}"

# Card Table
class Card(models.Model):

    account = models.CharField(max_length=20, default='AAA12345678')
    cnic = models.CharField(max_length=30,default='')
    card_number = models.CharField(max_length=20, unique=True)
    card_type = models.CharField(max_length=20)
    expiration_date = models.DateField(default=five_years_later)
    issue_date = models.DateField(default=today)
    cvv = models.CharField(max_length=3, default= str(random.randint(100, 500)))
    status = models.CharField(max_length=20, default='pending')
    online_tran = models.BooleanField(default=True)
    atm_withdrawal = models.BooleanField(default=True)
    pin = models.CharField(default='0000', max_length=4)

    def __str__(self):
        return f"{self.card_type} Card - {self.card_number}"


# Beneficiary Table
class Beneficiary(models.Model):
    ben_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=20)
    bank_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.account_number}"

