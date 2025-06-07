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

def generate_unique_card_number():
    while True:
        number = str(random.randint(10_000_000_000_000_00, 99_999_999_999_999_99))  # 8-digit number
        card_number = number
        if not Card.objects.filter(card_number=card_number).exists():
            return card_number


@login_required
@user_passes_test(not_superuser)
def net_dashboard(request):
    print(request.user)
    now_user = Customer.objects.get(user = request.user)
    try:
        card = Card.objects.get(account = now_user.account_number)
        cardslen = 1
    except:
        card=[]
        cardslen = 0
    month_expenses = 0
    month_income = 0
    incoming = Transaction.objects.filter(recipient_account = now_user.account_number)
    outgoing = Transaction.objects.filter(account = now_user.account_number)

    for tran in incoming:
        month_income = float(month_income) + float(tran.amount)

    for tran in outgoing:
        month_expenses = float(month_expenses) + float(tran.amount)

    cust = Customer.objects.get(user=request.user)
    acc = cust.account_number
    incoming = list(Transaction.objects.filter(recipient_account=cust.account_number))
    outgoing = list(Transaction.objects.filter(account=cust.account_number))
    transactions = incoming + outgoing
    transactions.sort(key=lambda x: x.id, reverse=True)
    transactions = transactions[:10]
    for tran in transactions:
        if tran.account == cust.account_number:
            rec_acc = tran.recipient_account
            rec_cust = Customer.objects.get(account_number = rec_acc)
            name = f'{rec_cust.first_name} {rec_cust.last_name}'
            tran.name = name
        else:
            sender_cust = Customer.objects.get(account_number=tran.account)
            name = f'{sender_cust.first_name} {sender_cust.last_name}'
            tran.name = name


    print('this is the customer', now_user.account_number)
    return render(request,'netbank/dashboard.html',{'cardslen':cardslen,'acc':acc,'user':now_user, 'month_exp':month_expenses,
                                                    'month_inc':month_income, 'card':card,'transactions':transactions})





@login_required
@user_passes_test(not_superuser)
def net_transfer(request):
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
                return redirect('net_trans_detail',trans_id = trans_id)
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
def net_trans_details(request,trans_id):
    transaction = Transaction.objects.get(trans_id = trans_id)
    sender_acc = transaction.account
    receiver_acc = transaction.recipient_account
    sender_customer = Customer.objects.get(account_number=sender_acc)
    receiver_customer = Customer.objects.get(account_number=receiver_acc)
    dic= {'trans':transaction,'sender':sender_customer,'receiver':receiver_customer}

    return render(request, 'netbank/trans_details.html',dic)


@login_required
@user_passes_test(not_superuser)
def test(request):
    return render(request,'netbank/test.html')


@login_required
@user_passes_test(not_superuser)
def user_block_card(request):
    cust = Customer.objects.get(user=request.user)
    card = Card.objects.get(account=cust.account_number)
    card.status = 'block'
    card.save()
    messages.error(request,"block")
    return redirect(f'/netbank/card_management/show_more/')



@login_required
@user_passes_test(not_superuser)
def user_active_card(request):
    cust = Customer.objects.get(user=request.user)
    card = Card.objects.get(account=cust.account_number)
    card.status = 'active'
    card.save()
    messages.error(request, "active")
    return redirect(f'/netbank/card_management/show_more/')



@login_required
@user_passes_test(not_superuser)
def user_change_atm_status(request):
    cust = Customer.objects.get(user=request.user)
    card = Card.objects.get(account=cust.account_number)
    card.atm_withdrawal = not card.atm_withdrawal
    card.save()
    messages.error(request, "atmstatus")
    return redirect(f'/netbank/card_management/show_more/')



@login_required
@user_passes_test(not_superuser)
def user_change_online_status(request):
    cust = Customer.objects.get(user=request.user)
    card = Card.objects.get(account=cust.account_number)
    card.online_tran = not card.online_tran
    card.save()
    messages.error(request, "onlinestatus")
    return redirect(f'/netbank/card_management/show_more/')


@login_required
@user_passes_test(not_superuser)
def user_view_card(request):
    cust = Customer.objects.get(user = request.user)
    try:
        card = Card.objects.get(account = cust.account_number)
        card_1 = card.card_number[:4]
        card_2 = card.card_number[4:8]
        card_3 = card.card_number[8:12]
        card_4 = card.card_number[12:]
        acc = Customer.objects.get(account_number = card.account)
        dic={'card':card,'card_1':card_1,'card_2':card_2,'card_3':card_3,'card_4':card_4,'acc':acc}
        return render(request,'netbank/user_view_card.html',dic)
    except:
        return render(request, 'netbank/apply_card.html')

@login_required
@user_passes_test(not_superuser)
def net_transactions(request):
    transactions = []
    print(1)
    if request.method == 'POST' and 'filter_search' in request.POST:
        print(2)
        datefrom = request.POST.get('datefrom','')
        dateto = request.POST.get('dateto','')
        if datefrom != '' and dateto != '':
            if dateto < datefrom:
                messages.error(request, 'dateerror')
            else:
                print(3)
                cust = Customer.objects.get(user=request.user)
                incoming = list(Transaction.objects.filter(recipient_account=cust.account_number, date__gte = datefrom, date__lte = dateto))
                outgoing = list(Transaction.objects.filter(account=cust.account_number, date__gte = datefrom, date__lte = dateto))
                transactions = incoming + outgoing
                transactions.sort(key=lambda x: x.id, reverse=True)
                return render(request, 'netbank/transactions.html',
                              {'transactions': transactions, 'acc': cust.account_number})
        elif datefrom != '' and dateto == '':
            print(4)
            cust = Customer.objects.get(user=request.user)
            incoming = list(
                Transaction.objects.filter(recipient_account=cust.account_number, date__gte=datefrom))
            outgoing = list(Transaction.objects.filter(account=cust.account_number, date__gte=datefrom))
            transactions = incoming + outgoing
            transactions.sort(key=lambda x: x.id, reverse=True)
            return render(request, 'netbank/transactions.html',
                          {'transactions': transactions, 'acc': cust.account_number})
        elif dateto != '' and datefrom == '':
            print(5)
            cust = Customer.objects.get(user=request.user)
            incoming = list(
                Transaction.objects.filter(recipient_account=cust.account_number, date__lte=dateto))
            outgoing = list(Transaction.objects.filter(account=cust.account_number, date__lte=dateto))
            transactions = incoming + outgoing
            transactions.sort(key=lambda x: x.id, reverse=True)
            return render(request, 'netbank/transactions.html',
                          {'transactions': transactions, 'acc': cust.account_number})


    print(6)
    cust = Customer.objects.get(user = request.user)
    incoming = list(Transaction.objects.filter(recipient_account = cust.account_number))
    outgoing = list(Transaction.objects.filter(account = cust.account_number))
    transactions = incoming + outgoing
    transactions.sort(key=lambda x: x.id, reverse=True)


    return render(request, 'netbank/transactions.html' ,{'transactions':transactions, 'acc':cust.account_number})


@login_required
@user_passes_test(not_superuser)
def user_profile(request):
    cust = Customer.objects.get(user=request.user)
    try:
        card = Card.objects.get(account=cust.account_number)
        is_card = True
    except:
        card = []
        is_card = False

    context = {
        'customer': cust,
        'card': card,
        'user': request.user,
        'is_card':is_card

    }
    return render(request, 'netbank/user_profile.html', context)


@login_required
@user_passes_test(not_superuser)
def apply_card(request):
    cust = Customer.objects.get(user=request.user)

    if request.method == 'POST' and 'classic' in request.POST:
        if apply_card_fun(request,'classic'):
            messages.error(request,'applied')
            return redirect('net_dashboard')
        else:
            return render(request, 'netbank/apply_card.html')
    elif request.method == 'POST' and 'gold' in request.POST:
        if apply_card_fun(request, 'gold'):
            messages.error(request, 'applied')
            return redirect('net_dashboard')
        else:
            return render(request, 'netbank/apply_card.html')
    elif request.method == 'POST' and 'platinum' in request.POST:
        if apply_card_fun(request, 'platinum'):
            messages.error(request, 'applied')
            return redirect('net_dashboard')
        else:
            return render(request, 'netbank/apply_card.html')




    if Card.objects.filter(cnic=cust.cnic).exists():
        messages.error(request,'already')
        return redirect('net_dashboard')
    else:
        return render(request,'netbank/apply_card.html')


@login_required
@user_passes_test(not_superuser)
def apply_card_fun(request,selectedType):
    cust = Customer.objects.get(user=request.user)
    Card.objects.create(account = cust.account_number,cnic = cust.cnic,card_number = generate_unique_card_number(), card_type = selectedType)
    return True


def change_pass(request):

    if request.method == 'POST':
        current_pass = request.POST.get('current_password')
        new_pass = request.POST.get('new_password')
        confirm_pass = request.POST.get('confirm_password')
        if request.user.check_password(current_pass):
            if new_pass == confirm_pass:
                request.user.set_password(new_pass)
                request.user.save()
                messages.error(request, 'passchange')
                return redirect('change_password')
            else:
                messages.error(request, 'notequal')
                return redirect('change_password')
        else:
            messages.error(request,'wrongpass')
            return redirect('change_password')


    return render(request,'netbank/change_password.html')






















