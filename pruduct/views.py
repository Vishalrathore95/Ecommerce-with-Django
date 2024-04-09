
from django.shortcuts import render
from pruduct.models import Product
from accounts.models import Profile




def get_product(request, slug):
    print('******')
    print(request.user)
    print('******')
    if hasattr(request.user, 'profile'):
        print(request.user.profile.get_cart_count)
    else:
        print("User has no profile.")
    product = Product.objects.get(slug=slug)
    context = {'product': product}
    
    if request.GET.get('size'):  
        size = request.GET['size']
        price = product.get_product_price_by_size(size)

        context['selected_size'] = size
        context['updated_price'] = price
    return render(request, 'products/product.html', context)



