from django.core.mail import send_mail
from . models import *
import json


def welcome_customer_email(email, username, raw_password):
    subject = 'Welcome to Store members'
    sender_email = 'rindra@hayramatechnology.com'
    message = (
        f'Dear {username},\n\n'
        f'Thank you for signing up on Django Store. We are excited to have you on board. Here are your account details:\n'
        f'Username: {username}\n'
        f'Password: {raw_password}\n\n'
        'You needn’t do anything at this point. Just enjoy your new account. Make sure to save this email for future reference.\n'
        f'Thank you for once again registering for our Store Site. In case of any questions, contact support {sender_email}.\n\n'
        'Best regards,\n'
        'Rindra, Django Store\n'
        'Harama Technology.'
    )
    recipient_email = email

    try:
        send_mail(
             subject,
             message,
             sender_email,
             [recipient_email],
             fail_silently=False,
        )
        print('Test email sent successfully!')
    except Exception as e:
        print('Failed to send test email:', e)

def send_payment_confirmation_email(email, username, Order_Total, shipping_address, shipping_state):
    subject = 'Payment Confirmation'
    sender_email = 'rindra@hayramatechnology.com'
    message = (
        f'Hi {username},\n\n'
        f'Thank you for your recent purchase with DJANGO STORE. Your order #Order_Number is confirmed. Here are the details:\n\n'
        f'Item(s): Item_List\n'
        f'Order total: ${Order_Total}\n'
        f'Estimated delivery date: [Delivery Date]\n'
        f'Shipping Address: {shipping_address}\n'
        f'Shipping State: {shipping_state}\n\n'
        f'Track your order is progress and view the details anytime by visiting [Order Tracking Link] or via your account.\n'
        f'If you are any questions or concerns, contact our customer support team {sender_email}.\n\n'
        'Thank you for shopping with us!'
    )
    recipient_email = email

    send_mail(
        subject,
        message,
        sender_email,
        [recipient_email],
        fail_silently=False,
    )

def guestCheckout(request):
    #set cart cookie
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    #get cart informations
    user = 'Guest'
    customer = []
    email = ''
    items = []
    order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
    cartItems = order['get_cart_items']
    for c in cart:
        # try if product exist or was deleted
        try:
            cartItems += cart[c]['quantity']
            product = Product.objects.get(id=c)
            total = (product.price * cart[c]['quantity'])
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[c]['quantity']
            #create product
            item = {
                    'product':{
                        'id':product.id,
                        'name':product.name,
                        'price':product.price,
                        'imageURL':product.imageURL
                    },
                    'quantity':cart[c]['quantity'],
                    'get_total':total,
            }
            #update items
            items.append(item)
            # saw if product if physical
            if product.digital == False:
                    order['shipping'] = True
        except:
            pass
    
    context = {
        'items':items,
        'order':order,
        'cartItems':cartItems,
        'user':user,
        'customer':customer,
        'email':email
    }

    return (context)

def customerCart(request):
    if request.user.is_authenticated:
        user = request.user
        customer = Customer.objects.get(user=user)
        email = customer.email
        # Get or create the order for the customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # Get all items for the order
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
          
     # if user not logged in
    else:
        cookieCart = guestCheckout(request)
        items = cookieCart['items']
        order = cookieCart['order']
        cartItems = cookieCart['cartItems']
        user = cookieCart['user']
        customer = cookieCart['customer']
        email = cookieCart['email']
    
    context = {
        'items':items,
        'order':order,
        'cartItems':cartItems,
        'user':user,
        'customer':customer,
        'email':email
    }

    return(context)

def guestOrder(request, data):
    name = data['form']['name']
    email = data['form']['email']

    #get cookie items
    cookieCart = guestCheckout(request)
    items = cookieCart['items']

    #create customer or check if email exist
    customers = Customer.objects.filter(email=email)
    if customers.exists():
        customer = customers[0]
    else:
        customer = Customer.objects.create(email=email, name=name)
    #customer, created = Customer.objects.get_or_create(email=email)
    #customer.name = name
    customer.save()

    #create order
    order = Order.objects.create(customer=customer, complete=False)

    #List all items and attach them to the order
    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderItems = OrderItem.objects.create(product=product, order=order, quantity=item['quantity'])

    context = {}

    return customer, order