from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Custumer)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(OrderPlaced)
admin.site.register(WishList)
