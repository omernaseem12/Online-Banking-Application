from django.shortcuts import render, HttpResponse, redirect,get_object_or_404
from django.contrib import messages
from admindash.models import Customer,Card,Transaction
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required, user_passes_test
import random
from datetime import date
# Create your views here.

today = date.today()

# Create your views here.

def dashboard(request):
    return render(request,'netbank/dashboard.html')
