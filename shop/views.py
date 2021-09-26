from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import DetailView
from django.http import JsonResponse
from django.contrib import messages
import json
from datetime import datetime
from .forms import NewUserForm
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.forms import AuthenticationForm
from  .models import *
from . utils import cookieCart,cookieData,guestOrder

# Create your views here.
def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("shop:index")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm
	return render (request=request, template_name="shop/register.html", context={"register_form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("shop:index")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="shop/login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.")
	return redirect("shop:index")

def customize(request):
    if request.method=="POST":
        name=request.POST.get('name')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        dimensions=request.POST.get('dimensions')
        img=request.POST.get('img')
        customize=Customize(name=name,phone=phone,email=email,dimensions=dimensions,img=img,date=datetime.today())
        customize.save()
    return render(request,'shop/customize.html')

def index(request):
    products= Artwork.objects.all()
    context={'products':products}
    return render(request,'shop/index.html',context)


class ArtworkDetailView(DetailView):
    model=Artwork
    template_name="shop/view.html"

def about(request):
    context={}
    return render(request,'shop/about.html',context)

def cart(request):
    data=cookieData(request)
    order=data['order']
    items=data['items']

    context={'items':items,'order':order}
    return render(request,'shop/cart.html',context)


def checkout(request):
    data=cookieData(request)
    order=data['order']
    items=data['items']

    context={'items':items,'order':order}
    return render(request,'shop/checkout.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Artwork.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('hi',safe=False)

def processOrder(request):
    transaction_id=datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
        zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('payment complete',safe=False)
