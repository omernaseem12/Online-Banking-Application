from django.contrib import admin

# Register your models here.
from .models import Customer,Transaction,Card,Beneficiary


admin.site.register(Customer)
admin.site.register(Transaction)
admin.site.register(Card)
admin.site.register(Beneficiary)