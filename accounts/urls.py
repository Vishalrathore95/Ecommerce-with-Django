
from django.urls import path

from accounts.views import login_page, register_page, activate_email ,shopping_cart ,add_to_card ,remove_card


urlpatterns = [
    
    path('login/', login_page, name='login'),
    path('shopping-cart/', shopping_cart, name='shopping_cart'),
    path('register/' , register_page , name="register"),
    path('activate/<email_token>/' , activate_email , name="activate_email"),
    path('add-to-card/<uid>/', add_to_card , name="add_to_card"),
    path('remove_card/<int:item_id>/', remove_card, name='remove_card'),
  


    
]
