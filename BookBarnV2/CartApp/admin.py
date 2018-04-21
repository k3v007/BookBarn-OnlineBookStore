from django.contrib import admin
from CartApp.models import Cart, BookOrder

# Register your models here.

class BookOrderAdmin(admin.ModelAdmin):
    list_display = ('book', 'cart', 'quantity')


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'total', 'active', 'order_date', 'payment_style', 'delivery_address', 'cardNumber')
    empty_value_display = 'N/A'

admin.site.register(BookOrder, BookOrderAdmin)
admin.site.register(Cart, CartAdmin)