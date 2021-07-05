from django.urls import path
from .views import *

app_name='core'

urlpatterns = [
    path('cart/',cart,name='cart'),
    path('',store,name='store'),
    path('update_Item/',updateItem,name='update_item'),
    path('process_order/',processOrder,name='process_order'),
    
    path('checkout/',checkout,name='checkout'),
]