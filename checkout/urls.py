from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('order/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
]
