from django.shortcuts import render, HttpResponse, redirect,get_object_or_404
from django.contrib import messages
from .models import Customer,Card,Transaction
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required, user_passes_test
import random

# Create your views here.

def is_superuser(user):
    return user.is_superuser




def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username','default')
        password = request.POST.get('password','default')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            if user.is_superuser:
                print('hello yes')
                login(request,user)
                return redirect('dashboard')
        else:
            print('hello NOoo')
            messages.error(request, "Invalid")
            return redirect('login_view')


    return render(request,'admindash/login.html')

def logout_view(request):
    logout(request)
    return redirect('login_view')


search = False
def generate_unique_account_number():
    prefix = "ACC"
    while True:
        number = str(random.randint(10_000_000, 99_999_999))  # 8-digit number
        acc_number = prefix + number
        if not Customer.objects.filter(account_number=acc_number).exists():
            return acc_number


def generate_unique_card_number():
    while True:
        number = str(random.randint(10_000_000_000_000_00, 99_999_999_999_999_99))  # 8-digit number
        card_number = number
        if not Card.objects.filter(card_number=card_number).exists():
            return card_number

def generate_unique_trans_id():
    prefix = "TRX"
    while True:
        num = str(random.randint(10_000_000, 99_999_999))  # 8-digit number
        trans = prefix + num
        if not Transaction.objects.filter(trans_id=trans).exists():
            return trans

@login_required
@user_passes_test(is_superuser)
def dashboard(request):
    return render(request,'admindash/dashboard.html')


@login_required
@user_passes_test(is_superuser)
def user_management(request):
    search = False
    customer = None
    if request.method == 'GET' and 'find_btn' in request.GET:
        print("1")
        query = request.GET.get('q')
        if query:
            customers = Customer.objects.filter(
                Q(cnic__icontains=query) | Q(email__icontains=query) | Q(phone_number__icontains=query)
            )
            print("2")
            if customers:
                for c in customers:
                    try:
                        c.active_loans = c.loans.filter(status='active').count()
                    except:
                        c.active_loans = 0
                search = True
                print("3")
                return render(request, 'admindash/user_management.html', {'customers': customers, 'search': search})
            else:
                print("4")
                customers = Customer.objects.all()[:6]
                for customer in customers:
                    customer.active_loans = customer.loans.filter(status='active').count()
                messages.error(request,"notfound")
                return render(request, 'admindash/user_management.html', {'customers': customers, 'search': search})

    customers = Customer.objects.all()[:6]
    return render(request,'admindash/user_management.html',{'customers':customers,'search':search})


@login_required
@user_passes_test(is_superuser)
def add_user(request):
    return render(request, 'admindash/add_user.html')

@login_required
@user_passes_test(is_superuser)
def add_user_fun(request):

    if request.method == 'POST':
        firstname = request.POST.get('firstName','default').capitalize()
        lastName = request.POST.get('lastName','default').capitalize()
        cnic = request.POST.get('cnic','default')
        phone = request.POST.get('phone','default')
        dob = request.POST.get('dob','default')
        email = request.POST.get('email','default')
        password = request.POST.get('password','default')
        c_password = request.POST.get('c_password','default')
        accountType = request.POST.get('accountType','default')
        address = request.POST.get('address','default').capitalize()
        print(firstname,lastName,cnic,phone,dob,email,password,c_password,address,accountType)
        if password == c_password:
            if Customer.objects.filter(cnic=cnic).exists():
                messages.error(request, "Error")
                return redirect('add_user')
            my_user = User.objects.create_user(email, email, password)
            my_user.save()
            Customer.objects.create(first_name=firstname, last_name=lastName, email=email, phone_number=phone,
                                    address=address, date_of_birth=dob, cnic=cnic, user=my_user,account_number=generate_unique_account_number(),
                                   account_type=accountType)
            messages.error(request, "success")
            return redirect('add_user')
        else:
            messages.error(request, "pass_error")
            return redirect('add_user')
    return redirect('add_user')



@login_required
@user_passes_test(is_superuser)
def edit_user(request,user_id):

    if request.method == 'POST':
        user = get_object_or_404(User, pk=user_id)
        customer = Customer.objects.get(user_id = user_id)
        firstname = request.POST.get('firstName', 'default').capitalize()
        lastName = request.POST.get('lastName', 'default').capitalize()
        cnic = request.POST.get('cnic', 'default')
        phone = request.POST.get('phone', 'default')
        dob = request.POST.get('dob', 'default')
        email = request.POST.get('email', 'default')
        password = request.POST.get('password', 'default')
        c_password = request.POST.get('c_password', 'default')
        accountType = request.POST.get('accountType', 'default')
        address = request.POST.get('address', 'default').capitalize()
        accountstatus = request.POST.get('status', 'default')
        balance = request.POST.get('balance', 'default')

        # print(firstname, lastName, cnic, phone, dob, email, password, c_password, address, accountType)
        if len(password) ==0:
            customer.first_name = firstname
            customer.last_name = lastName
            customer.cnic = cnic
            customer.phone_number = phone
            customer.date_of_birth = dob
            customer.email = email
            customer.account_type = accountType
            customer.address = address
            customer.status = accountstatus
            customer.balance = balance
            customer.save()
            messages.error(request, "success")
            if user.email == email:
                pass
            else:
                user.email = email



            return redirect(f'/admindash/user_management/')
        else:
            if password == c_password:
                customer.first_name = firstname
                customer.last_name = lastName
                customer.cnic = cnic
                customer.phone_number = phone
                customer.date_of_birth=dob
                customer.email=email
                user.username = email
                if user.email == email:
                    pass
                else:
                    user.email = email
                user.set_password(password)
                user.save()
                customer.account_type = accountType
                customer.address = address
                customer.status = accountstatus
                customer.balance = balance
                customer.save()
                messages.error(request, "success")
                return redirect(f'/admindash/user_management/')
            else:
                messages.error(request, "pass_error")
                return redirect(f'/admindash/user_management/')



    customer = Customer.objects.get(user_id = user_id)

    return render(request,'admindash/edit_user.html',{'customer':customer})



@login_required
@user_passes_test(is_superuser)
def transactions(request):
    if request.method == 'POST':
        searchby = request.POST.get('searchby','default')
        search = request.POST.get('search','default')
        datefrom = request.POST.get('datefrom','default')
        dateto = request.POST.get('dateto','default')
        transactiontype = request.POST.get('transactiontype','default')

        if searchby == 'cnic':
            print('cnic')
            try:
                customer = Customer.objects.get(cnic=search)
            except:
                messages.error(request, "notfound")
                return redirect('transactions')
            acc = customer.account_number
            transactions = Transaction.objects.filter(account = acc.upper())
            if len(transactions) ==0:
                messages.error(request, "notfound")
                return redirect('transactions')
            return render(request,"admindash/show_transactions.html", {'transactions':transactions,'customer':customer})
        elif searchby == 'transaction':
            print('trans')
            print(search.upper())
            transactions = Transaction.objects.filter(trans_id=search.upper())
            if len(transactions) ==0:
                messages.error(request, "notfound")
                return redirect('transactions')
            for trans in transactions:
                acco = trans.account
            customer = Customer.objects.get(account_number=acco)
            return render(request, "admindash/show_transactions.html", {'transactions': transactions,'customer':customer})
        else:
            print('acc')
            transactions = Transaction.objects.filter(account=search.upper())
            if len(transactions) ==0:
                messages.error(request, "notfound")
                return redirect('transactions')
            customer = Customer.objects.get(account_number=search.upper())
            return render(request, "admindash/show_transactions.html", {'transactions': transactions,'customer':customer})



    return render(request,"admindash/show_transactions.html")

@login_required
@user_passes_test(is_superuser)
def transaction_details(request,trans_id):
    transaction = Transaction.objects.get(trans_id = trans_id)
    sender_acc = transaction.account
    receiver_acc = transaction.recipient_account
    sender_customer = Customer.objects.get(account_number=sender_acc)
    receiver_customer = Customer.objects.get(account_number=receiver_acc)
    dic= {'trans':transaction,'sender':sender_customer,'receiver':receiver_customer}

    return render(request, 'admindash/trans_more.html',dic)




@login_required
@user_passes_test(is_superuser)
def del_user(request,user_id):
    try:
        user = User.objects.get(id = user_id)
    except:
        pass

    try:
        customer = Customer.objects.get(user = user)
    except:
        pass
    try:
        acc = customer.account_number
    except:
        pass
    try:
        card = Card.objects.get(account = acc)
        card.delete()
    except:
        pass
    customer.delete()
    user.delete()
    messages.error(request,'Successful')
    return redirect('user_management')




@login_required
@user_passes_test(is_superuser)
def card_management(request):

    if request.method == 'POST':
        search = request.POST.get('search').strip()
        status = request.POST.get('status').strip()
        type = request.POST.get('type').strip()

        if type == 'all' and status == 'all':
            pre_search = Card.objects.filter()
            print(1)
        elif type != 'all' and status == 'all':
            pre_search = Card.objects.filter(card_type=type)
            print(2)
        elif type == 'all' and status != 'all':
            pre_search = Card.objects.filter(status = status)
        else:
            pre_search = Card.objects.filter(status=status, card_type = type)

        print(pre_search,00000)
        cards = pre_search.filter((Q(card_number__icontains=search) |
            Q(account__icontains=search) |
            Q(cnic__icontains=search)))
        dic = {'cards': cards}
        print(cards,3)
        if len(cards) == 0:
            print(4)
            messages.error(request,'notfound')
            return redirect('card_management')
        for card in cards:
            card.first_4 = card.card_number[:4]
            card.last_4 = card.card_number[-4:]
            card.card_cust = Customer.objects.get(account_number=card.account)
            dic = {'cards': cards}

        return render(request, 'admindash/card_management.html', dic)

    cards = Card.objects.all()[:8]
    dic = {'cards': cards}
    for card in cards:
        card.first_4 = card.card_number[:4]
        card.last_4 = card.card_number[-4:]
        card.card_cust = Customer.objects.get(account_number = card.account)
        dic = {'cards': cards}

    return render(request,'admindash/card_management.html',dic)


@login_required
@user_passes_test(is_superuser)
def block_card(request,id):
    card = Card.objects.get(id=id)
    card.status = 'block'
    card.save()
    messages.error(request,"block")
    return redirect(f'/admindash/card_management/show_more/{id}/')




@login_required
@user_passes_test(is_superuser)
def active_card(request,id):
    card = Card.objects.get(id=id)
    card.status = 'active'
    card.save()
    messages.error(request, "active")
    return redirect(f'/admindash/card_management/show_more/{id}/')




@login_required
@user_passes_test(is_superuser)
def replace_card(request,id):
    card = Card.objects.get(id=id)
    card_type = card.card_type
    cust = Customer.objects.get(account_number = card.account)
    card.delete()
    Card.objects.create(account = cust.account_number,cnic=cust.cnic,card_number = generate_unique_card_number(),card_type = card_type, id=id)
    messages.error(request, "regen")
    return redirect(f'/admindash/card_management/show_more/{id}/')



@login_required
@user_passes_test(is_superuser)
def change_atm_status(request,id):
    card = Card.objects.get(id=id)
    card.atm_withdrawal = not card.atm_withdrawal
    card.save()
    messages.error(request, "atmstatus")
    return redirect(f'/admindash/card_management/show_more/{id}/')


@login_required
@user_passes_test(is_superuser)
def change_online_status(request,id):
    card = Card.objects.get(id=id)
    card.online_tran = not card.online_tran
    card.save()
    messages.error(request, "onlinestatus")
    return redirect(f'/admindash/card_management/show_more/{id}/')


@login_required
@user_passes_test(is_superuser)
def del_card(request,id):
    card = Card.objects.get(id=id)
    card.delete()
    messages.error(request, "del_card")
    return redirect(f'/admindash/card_management/')
@login_required
@user_passes_test(is_superuser)
def view_card(request,id):
    card = Card.objects.get(id = id)
    card_1 = card.card_number[:4]
    card_2 = card.card_number[4:8]
    card_3 = card.card_number[8:12]
    card_4 = card.card_number[12:]
    acc = Customer.objects.get(account_number = card.account)
    dic={'card':card,'card_1':card_1,'card_2':card_2,'card_3':card_3,'card_4':card_4,'acc':acc}
    return render(request,'admindash/view_card.html',dic)

@login_required
@user_passes_test(is_superuser)
def issue_card(request):
    dic = {}
    if request.method == 'POST':
        search = request.POST.get('search').strip()
        customers = Customer.objects.filter((
            Q(account_number__icontains=search) |
            Q(cnic__icontains=search)))
        dic = {'customers': customers}
        if len(customers) == 0:
            messages.error(request,'notfound')
            return redirect('issue_card')
        for customer in customers:
            customer.total_cards = len(Card.objects.filter(cnic = customer.cnic))
            customer.active_cards = len(Card.objects.filter(cnic = customer.cnic, status = 'active'))
            dic = {'customers': customers}
        return render(request, 'admindash/new_card.html', dic)

    return render(request,'admindash/new_card.html')

@login_required
@user_passes_test(is_superuser)
def issue_card_fun(request,customerId,selectedType):
    cust = Customer.objects.get(user_id=customerId)
    Card.objects.create(account = cust.account_number,cnic = cust.cnic,card_number = generate_unique_card_number(), card_type = selectedType)
    messages.error(request,'done')
    return redirect('issue_card')


@login_required
def fake_tran(request):
    trans_id = generate_unique_trans_id()
    account = 'ACC43544105'
    type = 'Deposit'
    amount = 2000
    description = "nothing"
    recipient_account = 'ACC32886858'
    Transaction.objects.create(trans_id=trans_id,amount=amount,account=account,type=type,description=description,recipient_account=recipient_account)
    return HttpResponse('Added')

