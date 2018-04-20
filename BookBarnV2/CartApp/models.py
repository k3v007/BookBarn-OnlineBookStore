from django.db import models
from django.contrib.auth.models import User
from BookBarnApp.models import Books
# from django.db.models.signals import pre_save, post_save, m2m_changed

# User = settings.AUTH_USER_MODEL
# Create your models here.

# class CartManager(models.Manager):

#     def new_or_get(self, request):
#         cart_id = request.session.get("cart_id", None)
#         qs=self.get_queryset().filter(id=cart_id)
#         if qs.count() == 1:                         
#             print('Cart ID exists.') 
#             new_obj = False                        
#             cart_obj = qs.first()
#             if request.user.is_authenticated and cart_obj.user is None:
#                 cart_obj.user=request.user
#                 cart_obj.save()
#         else:
#             cart_obj = Cart.objects.new(user=request.user)
#             new_obj = True
#             request.session['cart_id'] = cart_obj.id

#         return cart_obj, new_obj

#     def new(self, user=None):
#         user_obj=None
#         if user is not None:
#             if user.is_authenticated:
#                 user_obj=user
#         return self.model.objects.create(user=user_obj)

#     class Meta:
#         db_table = "cartmanager"
#         verbose_name = "CartManager"
#         verbose_name_plural = "CartManagers"

# class Cart(models.Model):
#     user = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)
#     products = models.ManyToManyField(Books, blank=True)
#     subtotal = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
#     total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
#     updated = models.DateTimeField(auto_now=True)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         db_table = 'cart'
#         verbose_name = 'Cart'
#         verbose_name_plural = 'Carts'

#     objects = CartManager()

#     def __str__(self):
#         return str(self.id)


# def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
#     if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
#         products = instance.products.all()
#         total = 0
#         for x in products:
#             total += x.price
#         print(total)
#         instance.subtotal = total
#         instance.save()
# m2m_changed.connect(m2m_changed_cart_receiver, sender = Cart.products.through)


# def pre_save_cart_receiver(sender, instance, *args, **kwargs):
#     delivery_charge = 30
#     if instance.subtotal > 0:
#         instance.total = instance.subtotal + delivery_charge
#     else:
#         instance.total = 0.00

# pre_save.connect(pre_save_cart_receiver, sender = Cart)


#########################################################################3

class Cart(models.Model):    
    PAYMENT_CHOICES = (
        ('CREDIT', 'Credit Card'),
        ('COD', 'Cash on Delivery')
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    order_date = models.DateField(null=True, blank=False, auto_now=True)
    payment_style = models.CharField(max_length=100, choices=PAYMENT_CHOICES, null=False, blank=False, default='COD')
    delivery_address = models.CharField(max_length=255, null=True, blank=False)
    
    class Meta:
        db_table = "cart"
        verbose_name = "Cart"
        verbose_name_plural = "Carts"

    def __str__(self):
        return str(self.id)

    def add_to_cart(self, isbn):
        book = Books.objects.get(pk=isbn)
        try:
            preexisting_order = BookOrder.objects.get(book=book, cart=self)
            preexisting_order.quantity += 1
            preexisting_order.save()
        except BookOrder.DoesNotExist:
            new_order = BookOrder.objects.create(
                book=book,
                cart=self,
                quantity=1
            )
            new_order.save()

    def remove_from_cart(self, isbn):
        book = Books.objects.get(pk=isbn)
        try:
            preexisting_order = BookOrder.objects.get(book=book, cart=self)
            if preexisting_order.quantity > 1:
                preexisting_order.quantity -= 1
                preexisting_order.save()
            else:
                preexisting_order.delete()
        except BookOrder.DoesNotExist:
            pass

    


class BookOrder(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        db_table = "bookorder"
        verbose_name = "BookOrder"
        verbose_name_plural = "BookOrders"