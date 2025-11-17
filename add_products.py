#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_store.settings')
django.setup()

from shop.models import Category, Product, ProductImage
from decimal import Decimal

def create_sample_products():
    # Create categories
    electronics = Category.objects.create(
        name='Electronics',
        slug='electronics',
        description='Latest electronic gadgets and devices'
    )

    clothing = Category.objects.create(
        name='Clothing',
        slug='clothing',
        description='Fashionable clothing for all occasions'
    )

    books = Category.objects.create(
        name='Books',
        slug='books',
        description='Bestselling books and literature'
    )

    # Create products
    products_data = [
        {
            'name': 'Wireless Bluetooth Headphones',
            'slug': 'wireless-bluetooth-headphones',
            'description': 'Premium noise-cancelling wireless headphones with 30-hour battery life and superior sound quality.',
            'price': Decimal('199.99'),
            'discount_price': Decimal('149.99'),
            'stock': 50,
            'category': electronics,
            'is_active': True,
            'is_featured': True
        },
        {
            'name': 'Smart Watch Pro',
            'slug': 'smart-watch-pro',
            'description': 'Advanced fitness tracking, heart rate monitoring, and smartphone integration in a sleek design.',
            'price': Decimal('299.99'),
            'discount_price': Decimal('249.99'),
            'stock': 30,
            'category': electronics,
            'is_active': True,
            'is_featured': True
        },
        {
            'name': 'Laptop Backpack',
            'slug': 'laptop-backpack',
            'description': 'Durable and stylish backpack with laptop compartment, USB charging port, and multiple pockets.',
            'price': Decimal('79.99'),
            'stock': 100,
            'category': electronics,
            'is_active': True,
            'is_featured': False
        },
        {
            'name': 'Designer T-Shirt',
            'slug': 'designer-t-shirt',
            'description': 'Premium cotton t-shirt with modern design and comfortable fit.',
            'price': Decimal('39.99'),
            'discount_price': Decimal('29.99'),
            'stock': 200,
            'category': clothing,
            'is_active': True,
            'is_featured': True
        },
        {
            'name': 'Classic Denim Jeans',
            'slug': 'classic-denim-jeans',
            'description': 'Timeless denim jeans with perfect fit and durable fabric.',
            'price': Decimal('89.99'),
            'stock': 150,
            'category': clothing,
            'is_active': True,
            'is_featured': False
        },
        {
            'name': 'Winter Jacket',
            'slug': 'winter-jacket',
            'description': 'Warm and stylish winter jacket with water-resistant coating.',
            'price': Decimal('159.99'),
            'discount_price': Decimal('129.99'),
            'stock': 80,
            'category': clothing,
            'is_active': True,
            'is_featured': True
        },
        {
            'name': 'Bestseller Novel',
            'slug': 'bestseller-novel',
            'description': 'Captivating story that has topped bestseller lists worldwide.',
            'price': Decimal('24.99'),
            'discount_price': Decimal('19.99'),
            'stock': 500,
            'category': books,
            'is_active': True,
            'is_featured': True
        },
        {
            'name': 'Programming Guide',
            'slug': 'programming-guide',
            'description': 'Comprehensive guide to modern programming practices and techniques.',
            'price': Decimal('49.99'),
            'stock': 100,
            'category': books,
            'is_active': True,
            'is_featured': False
        },
        {
            'name': 'Cookbook Collection',
            'slug': 'cookbook-collection',
            'description': 'Delicious recipes from around the world with step-by-step instructions.',
            'price': Decimal('34.99'),
            'stock': 75,
            'category': books,
            'is_active': True,
            'is_featured': True
        }
    ]

    # Create products
    for product_data in products_data:
        product = Product.objects.create(**product_data)
        print(f'Created product: {product.name}')

    print(f'\nCreated {Category.objects.count()} categories')
    print(f'Created {Product.objects.count()} products')

if __name__ == '__main__':
    create_sample_products()
