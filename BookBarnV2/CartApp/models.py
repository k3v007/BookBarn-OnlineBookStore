from django.db import models
from django.contrib.auth.models import User
from BookBarnApp.models import Books


class Cart(models.Model):    
    PAYMENT_CHOICES = (
        ('CREDIT', 'Credit Card'),
        ('COD', 'Cash on Delivery')
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    total = models.DecimalField(null=False, blank=True, default=0.0, max_digits=7, decimal_places=2)
    order_date = models.DateTimeField(null=True, blank=False, auto_now=True)
    payment_style = models.CharField(max_length=100, choices=PAYMENT_CHOICES, null=False, blank=False, default='COD')
    delivery_address = models.CharField(max_length=255, null=True, blank=False)
    cardNumber = models.CharField(max_length=16, null=True, blank=True)
    
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