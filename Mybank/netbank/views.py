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

def not_superuser(user):
    return not user.is_superuser



def generate_unique_trans_id():
    prefix = "TRX"
    while True:
        num = str(random.randint(10_000_000, 99_999_999))  # 8-digit number
        trans = prefix + num
        if not Transaction.objects.filter(trans_id=trans).exists():
            return trans



@login_required
@user_passes_test(not_superuser)
def dashboard(request):
    print(request.user)
    now_user = Customer.objects.get(user = request.user)
    month_expenses = 0
    month_income = 0
    incoming = Transaction.objects.filter(recipient_account = now_user.account_number)
    outgoing = Transaction.objects.filter(account = now_user.account_number)

    for tran in incoming:
        month_income = float(month_income) + float(tran.amount)

    for tran in outgoing:
        month_expenses = float(month_expenses) + float(tran.amount)


    print('this is the customer', now_user.account_number)
    return render(request,'netbank/dashboard.html',{'user':now_user, 'month_exp':month_expenses,'month_inc':month_income})





@login_required
@user_passes_test(not_superuser)
def transfer(request):
    cust = Customer.objects.get(user=request.user)
    if request.method == 'POST' and 'first' in request.POST:
        account = request.POST.get('from_account')
        bank = request.POST.get('recipient_bank')
        acc_num = request.POST.get('recipient_account')

        if not Customer.objects.filter(account_number = acc_num, status = 'Active').exists():
            messages.error(request,'notfound')
        else:
            receiver = Customer.objects.get(account_number = acc_num)
            print(receiver)
            return render(request, 'netbank/transfer2.html', {"cust": cust,'receiver':receiver,'bank':bank})

    if request.method == 'POST' and 'review' in request.POST:
        to_account = request.POST.get('to_account')
        amount = request.POST.get('amount')
        description = request.POST.get('description','')
        bank = request.POST.get('bank','')
        fees = 0
        rec_user = Customer.objects.get(account_number = to_account)
        if int(amount)> int(cust.balance):
            messages.error(request,'lowfunds')
            return render(request, 'netbank/transfer2.html', {"cust": cust, 'receiver': rec_user, 'bank': bank})
        return render(request,'netbank/transfer3.html',{'cust':cust,'amount':amount,'bank':bank,'description':description,'fees':fees,'rec_cust':rec_user,'total':int(fees)+int(amount)})

    if request.method == 'POST' and 'confirm' in request.POST:
        account = cust.account_number
        recipient_account = request.POST.get('to_account')
        amount = request.POST.get('amount')
        total = request.POST.get('total')

        description = request.POST.get('description')

        trans_id = generate_unique_trans_id()
        type = 'transfer'
        method = 'digital'
        try:
            if cust.status == 'Active':
                Transaction.objects.create(trans_id=trans_id, amount=amount, account=account, type=type,
                                           description=description, recipient_account=recipient_account, method = method)
                rec_user = Customer.objects.get(account_number=recipient_account)
                cust.balance = float(cust.balance) - float(total)
                cust.save()
                rec_user.balance = float(rec_user.balance) + float(amount)
                rec_user.save()
                return redirect('trans_detail',trans_id = trans_id)
            else:
                messages.error(request,'blocked')
                return render(request, 'netbank/transfer.html', {"cust": cust})
        except:
            print("error handle")
            messages.error(request,'error')
            return render(request,'netbank/transfer.html',{"cust":cust})

    elif request.method == 'POST' and 'back' in request.POST:
        return render(request, 'netbank/transfer.html', {"cust": cust})

    return render(request,'netbank/transfer.html',{"cust":cust})



@login_required
@user_passes_test(not_superuser)
def trans_details(request,trans_id):
    transaction = Transaction.objects.get(trans_id = trans_id)
    sender_acc = transaction.account
    receiver_acc = transaction.recipient_account
    sender_customer = Customer.objects.get(account_number=sender_acc)
    receiver_customer = Customer.objects.get(account_number=receiver_acc)
    dic= {'trans':transaction,'sender':sender_customer,'receiver':receiver_customer}

    return render(request, 'netbank/trans_details.html',dic)



def bills(request):
    return render(request,'netbank/bills.html')




