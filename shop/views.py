from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Category, Review
from cart.models import Cart, CartItem

def home(request):
    featured_products = Product.objects.filter(featured=True, available=True)[:8]
    new_arrivals = Product.objects.filter(available=True).order_by('-created')[:8]
    categories = Category.objects.all()
    
    context = {
        'featured_products': featured_products,
        'new_arrivals': new_arrivals,
        'categories': categories,
    }
    return render(request, 'shop/home.html', context)

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
    
    # Price filtering
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Sorting
    sort_by = request.GET.get('sort', 'created')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'name':
        products = products.order_by('name')
    else:
        products = products.order_by('-created')
    
    # Pagination
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    
    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'query': query,
        'min_price': min_price,
        'max_price': max_price,
        'sort_by': sort_by,
    }
    return render(request, 'shop/product_list.html', context)

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    
    # Get related products
    related_products = Product.objects.filter(category=product.category, available=True).exclude(id=product.id)[:4]
    
    # Get reviews
    reviews = product.reviews.all().order_by('-created')
    
    # Calculate average rating
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    
    # Check if product is in user's wishlist
    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = request.user.wishlist.products.filter(id=product.id).exists()
    
    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'in_wishlist': in_wishlist,
    }
    return render(request, 'shop/product_detail.html', context)

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Check if user has already reviewed this product
    if product.reviews.filter(user=request.user).exists():
        messages.warning(request, 'You have already reviewed this product.')
        return redirect('shop:product_detail', id=product.id, slug=product.slug)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        if rating and comment:
            Review.objects.create(
                product=product,
                user=request.user,
                rating=int(rating),
                comment=comment
            )
            messages.success(request, 'Your review has been submitted!')
        else:
            messages.error(request, 'Please provide both rating and comment.')
    
    return redirect('shop:product_detail', id=product.id, slug=product.slug)
