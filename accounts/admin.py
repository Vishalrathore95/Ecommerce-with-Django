from django.contrib import admin
from accounts.models import Profile ,Card ,CardItems

# Register your models here.
admin.site.register(Profile)
admin.site.register(Card)
admin.site.register(CardItems)
