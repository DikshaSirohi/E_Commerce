from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.db.models import Q
from .forms import CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm
from .models import UserProfile, Wishlist
from shop.models import Product

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('shop:home')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('shop:home')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created for {user.username}!')
            return redirect('shop:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    profile = request.user.profile
    wishlist = request.user.wishlist
    wishlist_products = wishlist.products.all()
    
    context = {
        'profile': profile,
        'wishlist_products': wishlist_products,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, 
                                       instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'accounts/edit_profile.html', context)

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist = request.user.wishlist
    wishlist.products.add(product)
    messages.success(request, f'{product.name} added to your wishlist!')
    return redirect('shop:product_detail', id=product.id, slug=product.slug)

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist = request.user.wishlist
    wishlist.products.remove(product)
    messages.success(request, f'{product.name} removed from your wishlist!')
    return redirect('accounts:profile')

@login_required
def order_history(request):
    orders = request.user.orders.all().order_by('-created')
    return render(request, 'accounts/order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(request.user.orders, id=order_id)
    return render(request, 'accounts/order_detail.html', {'order': order})
