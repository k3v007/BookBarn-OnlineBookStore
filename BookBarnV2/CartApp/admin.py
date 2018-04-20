from django.contrib import admin
from CartApp.models import Cart, BookOrder

# Register your models here.

class BookOrderAdmin(admin.ModelAdmin):
    list_display = ('book', 'cart', 'quantity')


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'active', 'order_date')

admin.site.register(BookOrder, BookOrderAdmin)
admin.site.register(Cart, CartAdmin)