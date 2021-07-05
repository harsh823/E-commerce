from django.shortcuts import render
from .models import*
from django.http import JsonResponse
import json
from .utils import cookieCart,cartData,guestOrder
import datetime
# Create your views here.


def store(request):
    data=cartData(request)
    cartItems=data['cartItems']
    
    products=Product.objects.all()
    context={'products':products,'cartItems':cartItems}
    return render(request,'core/store.html' ,context)

def checkout(request):
    
    data=cartData(request)
    cartItems=data['cartItems']
    order=data['order']
    items=data['items']
    context={'items':items,'order':order,'cartItems':cartItems,'shipping':False}
    return render(request,'core/checkout.html',context)    

def cart(request):
    data=cartData(request)
    cartItems=data['cartItems']
    order=data['order']
    items=data['items']
    

    context={'items':items,'order':order,'cartItems':cartItems,'shipping':False}
    return render(request,'core/cart.html',context)    

def updateItem(request):
    data=json.loads(request.body)
    productId=data['productId']
    action=data['action']
    
    customer=request.user.customer
    product=Product.objects.get(id=productId)
    order,create=Order.objects.get_or_create(customer=customer,complete=False)
    orderitem,create=OrderItem.objects.get_or_create(order=order,product=product)
    if action=='add':
        orderitem.quantity=(orderitem.quantity+1)
    elif action=='remove':
        orderitem.quantity=(orderitem.quantity-1)
    orderitem.save()
    if orderitem.quantity<=0:
        orderitem.delete()   
            
    return JsonResponse('Item is added',safe=False)

def processOrder(request):
    transaction_id=datetime.datetime.now().timestamp()
    data=json.loads(request.body)

    if request.user.is_authenticated:
        customer=request.user.customer
        order,create=Order.objects.get_or_create(customer=customer,complete=False)
   
    else:
        customer,order=guestOrder(request,data)
           
    total=float(data['form']['total'])
    order.transaction_id=transaction_id
    if total == order.get_cart_total:
        order.complete=True
    order.save()

    if order.shipping==True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
    return JsonResponse('payment Completed',safe=False)    