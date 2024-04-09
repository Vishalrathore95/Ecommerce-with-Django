from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.http import HttpResponseRedirect, HttpResponse
from .models import Profile
from pruduct.models import *
from django.conf import settings
from accounts.models import Card,CardItems
from django.http import HttpResponseRedirect
from base.emails import send_account_activation_email
import uuid
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum







def login_page(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user_obj = User.objects.get(username=email)
        except User.DoesNotExist:
            messages.warning(request, 'Account not found.')
            return HttpResponseRedirect(request.path_info)
        
        try:
            is_email_verified = user_obj.profile.is_email_verified
        except ObjectDoesNotExist:
           
            messages.warning(request, 'Profile not found for this account.')
            return HttpResponseRedirect(request.path_info)

        if not is_email_verified:
            messages.warning(request, 'Your account is not verified.')
            return HttpResponseRedirect(request.path_info)

        user_obj = authenticate(username=email, password=password)
        if user_obj:
            login(request, user_obj)
            return redirect('/')

        messages.warning(request, 'Invalid credentials')
        return HttpResponseRedirect(request.path_info)

    return render(request, 'accounts/login.html')


def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
       
        if User.objects.filter(username=email).exists():
            messages.warning(request, 'Email is already taken.')
            return HttpResponseRedirect(request.path_info)

       
        user_obj = User.objects.create_user(username=email, email=email, password=password,first_name=first_name, last_name=last_name)
        
       
        email_token = str(uuid.uuid4())
       
        try:
            profile = Profile.objects.get(user=user_obj)
            profile.email_token = email_token
            profile.save()
        except Profile.DoesNotExist:
            Profile.objects.create(user=user_obj, email_token=email_token)
        
        
        send_account_activation_email(email, email_token)

        messages.success(request, 'An email has been sent to activate your account.')
        return HttpResponseRedirect(request.path_info)

    return render(request, 'accounts/register.html')


def activate_email(request, email_token):
    try:
        profile = Profile.objects.get(email_token=email_token)
        
        
        profile.is_email_verified = True
        
     
        profile.save()
        
       
        return redirect('/')
    except Profile.DoesNotExist:
      
        return HttpResponse('Invalid Email token')
 
 
 
 
def add_to_card(request, uid):
    variant = request.GET.get('variant')
    
    product = Product.objects.get(uid=uid)
    user = request.user
    card, _ = Card.objects.get_or_create(user=user, is_paid=False)
    
    card_item = CardItems.objects.create(card=card, product=product )
    
    if variant:
       
        size_variant = SizeVariant.objects.get(size_name=variant)
        card_item.size_variant = size_variant
        card_item.save()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def remove_card(request,item_id ):
    try:
        cart_item = CardItems.objects.get(pk=item_id)
        cart_item.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except CardItems.DoesNotExist:
       
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
       
        print(e)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    
    


        


def shopping_cart(request):
    card_items = CardItems.objects.filter(card__is_paid=False, card__user=request.user)
    
    
    total_price = card_items.aggregate(total_price=Sum('product__price'))['total_price'] or 0
    
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon')
        
        coupon_obj = Coupon.objects.filter(coupon_code__iexact=coupon_code).first()
        
        if not coupon_obj:
            messages.warning(request, "Coupon code does not exist")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
       
        if total_price < coupon_obj.minimum_amount:
            messages.warning(request, "Total price should be greater than minimum amount")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
        for card_item in card_items:
            card_item.coupon = coupon_obj
            card_item.save()
       
        messages.success(request, "Coupon applied")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
    context = {'card_items': card_items, 'total_price': total_price}
    return render(request, 'products/coupon.html', context)


