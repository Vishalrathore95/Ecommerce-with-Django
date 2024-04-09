from django.db import models

from django.contrib.auth.models import User
from base.models import BaseModel

from django.db.models.signals import post_save
from django.dispatch import receiver

import uuid
from base.emails import send_account_activation_email
from pruduct.models import Product
from pruduct.models import ColorVariant
from pruduct.models import SizeVariant
from pruduct.models import Coupon




class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_email_verified = models.BooleanField(default=False)  
    email_token = models.CharField(max_length=100, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile')  
    
    def get_cart_count(self):
        return CardItems.objects.filter(card__user=self.user, card__is_paid=False).count()

       
class Card(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')  
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    is_paid= models.BooleanField(default=False) 
    
    def get_cart_total(self):
        cart_items = self.card_items.all()
        prices = []

        for cart_item in cart_items:
            product_price = cart_item.get_product_price()
            prices.append(product_price)
        if self.coupon:
            return sum(prices)- self.coupon.discount
        return sum(prices)
     
    

class CardItems(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='card_items')
   
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='card_items')
    color_variant = models.ForeignKey(ColorVariant, on_delete=models.SET_NULL, null=True, blank=True)
    size_variant = models.ForeignKey(SizeVariant, on_delete=models.SET_NULL, null=True, blank=True) 
    
    
    def get_product_price(self):
        price = [self.product.price]

        if self.color_variant:
            color_variant_price = self.color_variant.price
            price.append(color_variant_price)

        if self.size_variant:
            size_variant_price = self.size_variant.price
            price.append(size_variant_price)
       
        return sum(price)   
    
    
    
    
    
    
    
@receiver(post_save, sender=User)
def send_email_token(sender, instance, created, **kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            Profile.objects.create(user=instance, email_token=email_token)
            email = instance.email
            send_account_activation_email(email, email_token)
    except Exception as e:
        print(e)
    