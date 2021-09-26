import json
from .models import *

def cookieCart(request):
    try:
        cart=json.loads(request.COOKIES['cart'])
    except:
        cart={}

    print('Cart:',cart)
    items=[]
    order={'get_cart_items':0,'get_cart_total':0}

    for i in cart:
        try:
            product=Artwork.objects.get(id=i)
            total=(product.price * cart[i]['quantity'])
            order['get_cart_total']+=total
            order['get_cart_items']+=cart[i]['quantity']

            item={
                'product':{
                     'id':product.id,
                     'name':product.art_name,
                     'price':product.price,
                     'imageURL':product.imageURL,
                 },
                'quantity':cart[i]['quantity'],
                'get_total':total
            }
            items.append(item)
        except:
            pass

    return{'order':order,'items':items}

def cookieData(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
    else:
        cookieData=cookieCart(request)
        order=cookieData['order']
        items=cookieData['items']
    return{'order':order,'items':items}

def guestOrder(request,data):
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(
            email=email,
            )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
        )

    for item in items:
        product = Artwork.objects.get(id=item['product']['id'])
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=(item['quantity'] if item['quantity']>0 else -1*item['quantity']),
        )
    return customer, order
