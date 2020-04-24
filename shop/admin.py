from django.contrib import admin

# Register your models here.
from .models import Product, Contact, Orderproduct, OrderUpdate, Testmodel
admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Orderproduct)
admin.site.register(OrderUpdate)
admin.site.register(Testmodel)



