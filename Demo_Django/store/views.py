from django.shortcuts import render
from . models import *
#json
import json
from django.http import JsonResponse

import datetime

#utils.py for sending email, and guest checkout
from . utils import send_payment_confirmation_email, welcome_customer_email, customerCart, guestOrder

# user login/singin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect

from decimal import Decimal


def home(request):
     context = {}
     return render(request, 'store/base.html', context)

def store(request):
     cartData = customerCart(request)
     items = cartData['items']
     cartItems = cartData['cartItems']
     user = cartData['user']

     products = Product.objects.all()
     context = {'products':products, 'cartItems':cartItems, 'items':items, 'user':user}
     return render(request, 'store/store.html', context)

def products_items(request):
     cartData = customerCart(request)
     items = cartData['items']
     order = cartData['order']
     cartItems = cartData['cartItems']
     user = cartData['user']

     products = Product.objects.all()
     context = {'products':products, 'cartItems':cartItems, 'items':items, 'order':order, 'user':user}
     return render(request, 'store/products.html', context)

def cart(request):
     cartData = customerCart(request)
     items = cartData['items']
     order = cartData['order']
     cartItems = cartData['cartItems']
     user = cartData['user']
     
     context = {'cartItems':cartItems, 'order':order, 'items':items, 'user':user}
     return render(request, 'store/cart.html', context)

def updateItem(request):
     data = json.loads(request.body)
     productId = data['productId']
     action = data['action']
     
     print('productId:', productId)
     print('Action:', action)
     
     customer = request.user.customer
     product = Product.objects.get(id=productId)

     order, created = Order.objects.get_or_create(customer=customer, complete=False)
     orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
     
     if action == 'add':
          orderItem.quantity = (orderItem.quantity + 1)
     elif action == 'remove':
          orderItem.quantity = (orderItem.quantity - 1)
          
     orderItem.save()
     
     if orderItem.quantity <=0:
          orderItem.delete()
     
     response = JsonResponse('success add', safe=False)
     #response.set_cookie('cart', value=json.dumps(cart), max_age=604800, SameSite=None, secure=True)
     return response

def checkout(request):
     cartData = customerCart(request)
     items = cartData['items']
     order = cartData['order']
     cartItems = cartData['cartItems']
     customer = cartData['customer']
     email = cartData['email']
     user = cartData['user']
     
     context = {'items':items, 'order':order, 'cartItems':cartItems, 'customer':customer, 'email':email, 'user':user}

     return render(request, 'store/checkout.html', context)

def processOrder(request):
     transaction_id = datetime.datetime.now().timestamp()
     data = json.loads(request.body)

     if request.user.is_authenticated:
          customer = request.user.customer
          customers = Customer.objects.filter(email=data['form']['email'])
          if customers.exists():
               customer = customers[0]
               order, created = Order.objects.get_or_create(customer=customer, complete=False)
          else:
               order, created = Order.objects.get_or_create(customer=customer, complete=False)

     else:
          customer, order = guestOrder(request, data)

     total = Decimal(data['form']['total'])
     order.transaction_id = transaction_id

     if abs(total - order.get_cart_total) < Decimal('0.01'):
          order.complete = True

     if order.shipping == True:
          ShippingAddress.objects.create(
               customer=customer,
               order=order,
               address=data['shipping']['address'],
               city=data['shipping']['city'],
               state=data['shipping']['state'],
               zipcode=data['shipping']['zipcode'],
          )
                    
     order.save()
     send_payment_confirmation_email(
          data['form']['email'],
          data['form']['name'],
          data['form']['total'],
          data['shipping']['address'],
          data['shipping']['state']
     )
 
     response = JsonResponse('Payment submitted!',safe=False)
     #response.set_cookie('cart', value=json.dumps(cart), max_age=604800, SameSite=None, secure=True)
     return response

#user login
def user_login(request):
     cartData = customerCart(request)
     items = cartData['items']
     order = cartData['order']
     cartItems = cartData['cartItems']
     customer = cartData['customer']
     user = cartData['user']
     
     context = {'items':items, 'order':order, 'cartItems':cartItems, 'customer':customer}

     #login user section
     if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
               login(request, user)
               return redirect("store")
        else:
          return render(request, 'store/login.html', context)
     else:
          return render(request, 'store/login.html', context)

#user sign in
class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize widget attributes to add CSS classes
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

def user_signup(request):
     cartData = customerCart(request)
     items = cartData['items']
     order = cartData['order']
     cartItems = cartData['cartItems']
     customer = cartData['customer']
     user = cartData['user']
     
     if request.method == 'POST':
          customer_email = request.POST.get('customer_email')          
          form = CustomUserCreationForm(request.POST)
          if form.is_valid():
               user = form.save()
               username = form.cleaned_data.get('username')
               raw_password = form.cleaned_data.get('password1')
               user = authenticate(username=username, password=raw_password)
               if user is not None:
                    customer, created = Customer.objects.get_or_create(user=user, name=user, email=customer_email) #if Customer.DoesNotExist
                    login(request, user)
                    welcome_customer_email(customer_email, username, raw_password)
                    return redirect("store")

     else:
        form = CustomUserCreationForm()

     context = {'form': form, 'items':items, 'order':order, 'cartItems':cartItems, 'customer':customer}

     return render(request, 'store/signup.html', context)

#user logout
def user_logout(request):
    logout(request)
    return redirect("store")

