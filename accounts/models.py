from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=250, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True)
    newsletter_subscribed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_full_address(self):
        if self.address and self.city and self.country:
            return f"{self.address}, {self.city}, {self.country}"
        return "No address provided"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Wishlist(models.Model):
    user = models.OneToOneField(User, related_name='wishlist', on_delete=models.CASCADE)
    products = models.ManyToManyField('shop.Product', related_name='wishlists', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Wishlist"
    
    def get_product_count(self):
        return self.products.count()

@receiver(post_save, sender=User)
def create_user_wishlist(sender, instance, created, **kwargs):
    if created:
        Wishlist.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_wishlist(sender, instance, **kwargs):
    try:
        instance.wishlist.save()
    except Wishlist.DoesNotExist:
        Wishlist.objects.create(user=instance)
