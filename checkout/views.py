from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
import stripe
from cart.models import Cart, CartItem, Order, OrderItem, Payment
from cart.views import get_or_create_cart
from shop.models import Product

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def checkout(request):
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    
    if not cart_items:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart:cart_detail')
    
    # Check stock availability
    for item in cart_items:
        if not item.product.is_in_stock() or item.quantity > item.product.stock:
            messages.error(request, f'Sorry, {item.product.name} is out of stock or insufficient quantity.')
            return redirect('cart:cart_detail')
    
    total_cost = sum(item.get_total_price() for item in cart_items)
    shipping_cost = cart.get_shipping_cost() if hasattr(cart, 'get_shipping_cost') else (0 if total_cost >= 50 else 5.99)
    final_total = total_cost + shipping_cost
    
    if request.method == 'POST':
        # Get shipping information
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        postal_code = request.POST.get('postal_code')
        city = request.POST.get('city')
        country = request.POST.get('country')
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
            postal_code=postal_code,
            city=city,
            country=country,
            paid=False
        )
        
        # Create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.get_display_price(),
                quantity=item.quantity
            )
            # Update product stock
            item.product.stock -= item.quantity
            item.product.save()
        
        # Create payment intent
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(final_total * 100),  # Convert to cents
                currency='usd',
                metadata={'order_id': order.id},
                payment_method_types=['card']
            )
            
            # Create payment record
            payment = Payment.objects.create(
                order=order,
                stripe_payment_intent_id=intent.id,
                amount=final_total,
                status='pending'
            )
            
            order.stripe_payment_intent_id = intent.id
            order.save()
            
            context = {
                'order': order,
                'client_secret': intent.client_secret,
                'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
                'final_total': final_total,
            }
            return render(request, 'checkout/payment.html', context)
            
        except stripe.error.StripeError as e:
            messages.error(request, f'Payment error: {str(e)}')
            return redirect('checkout:checkout')
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_cost': total_cost,
        'shipping_cost': shipping_cost,
        'final_total': final_total,
        'user_profile': request.user.profile,
    }
    return render(request, 'checkout/checkout.html', context)

def payment_success(request):
    payment_intent_id = request.GET.get('payment_intent')
    if not payment_intent_id:
        messages.error(request, 'Invalid payment.')
        return redirect('shop:home')
    
    try:
        # Retrieve payment intent from Stripe
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        
        if intent.status == 'succeeded':
            # Find and update payment
            payment = Payment.objects.get(stripe_payment_intent_id=payment_intent_id)
            payment.mark_as_succeeded()
            
            # Clear cart
            cart = get_or_create_cart(request)
            cart.items.all().delete()
            
            messages.success(request, 'Payment successful! Your order has been placed.')
            return redirect('checkout:order_confirmation', order_id=payment.order.id)
        else:
            messages.error(request, 'Payment was not successful.')
            return redirect('cart:cart_detail')
            
    except stripe.error.StripeError as e:
        messages.error(request, f'Payment verification error: {str(e)}')
        return redirect('cart:cart_detail')

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'checkout/order_confirmation.html', {'order': order})
