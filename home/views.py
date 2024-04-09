from django.shortcuts import render


from pruduct.models import Product

def index(request):
    
    context ={'products': Product.objects.all()}
    return render(request, 'home/index.html', context)
