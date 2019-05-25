from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Contact, Feature_Product, Order, OrderUpdate, UserProfile
from PayTm import Checksum
from math import ceil
import json

cateprod = Product.objects.values('cate')
cates = {item['cate'] for item in cateprod}

MERCHANT_KEY = 'Your Merchant KEY'

def index(request):   
    """Fetch the all product from database and show the product category wise on home page""" 
    feat_prods = Feature_Product.objects.all()[::-1]
    allProd = []
    for cate in cates:
        prod = Product.objects.filter(cate=cate)[::-1]
        n = len(prod)
        nSlides = n//4 + ceil((n/4) - (n//4))
        allProd.append([prod, nSlides])
    context = {'allProd':allProd, 'feat_prods':feat_prods, 'cate':cates}            
    return render(request, 'shop/index.html', context)

def category(request, cate):
    """Show the product category wise"""
    prod = Product.objects.filter(cate=cate)
    context = {'cate':cates, 'prod':prod,'cate_name':cate}
    return render(request, 'shop/category.html', context)

def about(request):
    """About page of shopapp"""
    return render(request, 'shop/about.html', {'cate':cates})

def contact(request):
    """Contact page of shopapp"""
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        msg = request.POST.get('msg')
        contact = Contact(name=name, email=email, phone=phone, msg=msg)
        contact.save()
        messages.success(request, 'Your details has been submitted. We will response you very soon. Thank you so much.')
    return render(request, 'shop/contact.html', {'cate':cates}) 

def product(request, myid):
    """Show the product detail on Product page"""
    product = Product.objects.filter(id=myid)
    context = {'i':product[0],'cate':cates}
    return render(request, 'shop/product.html', context)

def search(request):
    """Search the product"""
    if 'search' in request.GET:
        search_prod = request.GET["search"]
        cate = search_prod.capitalize()
        prod = Product.objects.filter(cate=cate)
        if not prod:
            prod = Product.objects.filter(Q(product_name__icontains=search_prod)|
                Q(cate__icontains=search_prod)|Q(subcate__icontains=search_prod))     
            if not prod:
                messages.info(request,"Sorry, no results found!")
        context = {'prod':prod,'search_prod':search_prod, 'cate':cates}
        return render(request, 'shop/search.html',context)    

def tracker(request):
    """Track the order using Id and phone number in Tracker page"""
    if request.method == "POST":
        order_id = request.POST.get('orderId')
        phone = request.POST.get('phone')
        try:
            order = Order.objects.filter(id=order_id, phone=phone)
            if len(order)>0:
                update = OrderUpdate.objects.filter(OrderId=order_id)
                updates = []
                for item in update:
                    time = item.timestamp
                    updates.append({'text':item.update_desc,'time':time.strftime("%d %b %Y, %I:%M %p")})
                    response = json.dumps({'status':'success','update':updates,'order':order[0].cartItem}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"NoOrder"}')       
        except Exception as e:
            return HttpResponse('{"status":"error"}')
    return render(request, 'shop/tracker.html', {'cate':cates})
    
def order_tracker(request, order_id):
    """Order tracker in user order page"""
    order = Order.objects.filter(id=order_id)
    if len(order)>0:
        update = OrderUpdate.objects.filter(OrderId=order_id)
        updates = []
        for item in update:
            time = item.timestamp
            updates.append({'text':item.update_desc,'time':time.strftime("%d %b %Y, %I:%M %p")})
            response = json.dumps({'update':updates}, default=str)
        return HttpResponse(response)    
    else:
        return HttpResponse('Error')    

def cart(request):
    """Show the product in cart"""
    return render(request, 'shop/cart.html', {'cate':cates})    

@login_required(login_url='/shop/login/')
def checkout(request):
    """Place the order in checkout page"""
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        itemsJson = request.POST.get('itemsJson')
        cartItem = request.POST.get('cartItem')
        amount = request.POST.get('amount')
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')

        if (name and email):
            order = Order(user_id=user_id, items_json=itemsJson, cartItem=cartItem, amount=amount, name=name, email=email, address=address, 
                country=country, state=state, city=city, zip_code=zip_code, phone=phone)
            order.save()

        id = request.POST.get('userId')    

        uprofile = UserProfile.objects.filter(user_id=id)

        if uprofile:
            profile = uprofile[0]              

            itemsJson = request.POST.get('itemsJson1')
            cartItem = request.POST.get('cartItem1')
            amount = request.POST.get('amount1')

            order = Order(user_id=id, items_json=itemsJson, cartItem=cartItem, amount=amount, name=profile.name, email=profile.email, address=profile.address, 
                country=profile.country, state=profile.state, city=profile.city, zip_code=profile.zip_code, phone=profile.phone)
            order.save()

        update = OrderUpdate(OrderId=order.id, update_desc="The order has been placed")
        update.save()

        order_id = order.id
        if uprofile:
            profile = uprofile[0]    
            cust_email = profile.email
        else:
            cust_email = email    

        # paytm request for accept order payment
        
        param_dict = {
            'MID':'Your Merchant ID',
            'ORDER_ID':str(order_id),
            'TXN_AMOUNT':str(amount[1:]),
            'CUST_ID':cust_email,
            'INDUSTRY_TYPE_ID':'Retail',
            'WEBSITE':'WEBSTAGING',
            'CHANNEL_ID':'WEB',
            'CALLBACK_URL':f'http://127.0.0.1:8000/shop/handlerequest/{id}',
        }        
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)

        return render(request, 'shop/paytm.html', {'param_dict':param_dict})

    return render(request, 'shop/checkout.html',{'cate':cates})

def register(request):
    """User create the account in shopapp for place the order"""
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(f'/shop/profile/{user.id}')
        else:
            for msg in form.error_messages:
                messages.error(request, f'{form.error_messages[msg]}') 
    form = UserRegisterForm
    context = {'cate':cates,'form':form}
    return render(request, 'shop/register.html', context)  

def login_user(request):
    """User can login using username and password"""
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                return redirect(f'/shop/profile/{user.id}')  
        else:
            messages.error(request, 'Invalid Username and Password')        
    form = AuthenticationForm()
    context = {'cate':cates,'form':form}
    return render(request, 'shop/login.html', context)

def logout_user(request):
    """User logout function"""
    logout(request)
    return redirect('/shop/login/')

def profile(request, id):  
    """Show the user profile detail and user can add the profile details"""    
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        username = request.POST.get('username')
        name = request.POST.get('name')
        email = request.POST.get('useremail')
        address = request.POST.get('address')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')
        profile = UserProfile(user_id=user_id, username=username, name=name, email=email,
            address=address, country=country, state=state, city=city,zip_code=zip_code, phone=phone)
        profile.save()
    uprofile = UserProfile.objects.filter(user_id=id)
    if uprofile:
        context = {'cate':cates,'profile':uprofile[0]}
    else:    
        new_user = True
        context = {'cate':cates, 'new_user':new_user}
    return render(request, 'shop/profile.html', context)

def update_profile(request, id):
    """User update the profile details"""
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        username = request.POST.get('username')
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')

        user = User.objects.filter(id=id)
        user_info = user[0]
        user_info.email = email
        user_info.save()
        
        uprofile = UserProfile.objects.filter(user_id=id)
        profile = uprofile[0]

        profile.name = name
        profile.email = email
        profile.address = address
        profile.country = country
        profile.state = state
        profile.city = city
        profile.zip_code = zip_code
        profile.phone = phone

        profile.save()
        messages.success(request, 'Your Profile Updated')
        return redirect(f'/shop/profile/{id}')  

    uprofile = UserProfile.objects.filter(user_id=id)
    context = {'cate':cates,'profile':uprofile[0]}
    return render(request, 'shop/update.html', context)       

def order(request, id):
    """Show the order details in user order page"""
    order = Order.objects.filter(user_id=id)[::-1]
    if order:
        order_details = []
        for i in order:
            data = json.loads(i.cartItem)
            prod_list = []
            for key in data:
                key_id = key[2:]
                prod = Product.objects.filter(id=key_id)
                prod_detail = prod[0]
                qty = data[key][0:1]
                prod_list.append([prod_detail,qty])
            order_details.append([i,data,prod_list])  
        context = {'cate':cates,'data':order_details}
        return render(request, 'shop/order.html', context) 
    else:
        context = {'cate':cates}
        return render(request, 'shop/order.html', context)       

@csrf_exempt
def handlerequest(request,id):
    user = User.objects.filter(id=id)
    user.is_authenticated = True
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == "CHECKSUMHASH":
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            success = True
            return render(request, 'shop/paymentsuccess.html', {'response': response_dict,'cate':cates,
                'user':user[0],'user.is_authenticated':user.is_authenticated,'success':success})
        else:
            msg = 'Order was not successful because ' + response_dict['RESPMSG']
            return render(request, 'shop/paymentsuccess.html', {'response': response_dict,'cate':cates,
                'user':user[0],'user.is_authenticated':user.is_authenticated,'msg':msg})