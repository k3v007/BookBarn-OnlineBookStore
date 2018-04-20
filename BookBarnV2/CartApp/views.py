from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Cart, BookOrder
from BookBarnApp.models import Books
from .forms import CheckoutForm, NewAddressForm, CardForm

# Create your views here.

# def cartHomeView(request):
#     cart_obj, new_obj = Cart.objects.new_or_get(request)
#     print("XOXOXOXO")
#     print(cart_obj)
#     print("TOTOTOTO")
#     return render(request, "CartApp/home.html", {"cart":cart_obj})

# def cartUpdateView(request):
#     product_id = request.POST.get('product_id')
#     if product_id is not None:
#         try:
#             product_obj = Books.objects.get(isbn = product_id)
#         except Books.DoesNotExist:
#             print("Product is gone?")
#             return redirect("CartApp:cartHomeView")

#     cart_obj, new_obj = Cart.objects.new_or_get(request)
#     if product_obj in cart_obj.products.all():
#         cart_obj.products.remove(product_obj)
#     else:
#         cart_obj.products.add(product_obj)
#     request.session['cart_items'] = cart_obj.products.count()
#     # return redirect(product_obj.get_absolute_url())
#     return redirect("CartApp:cartHomeView")
    

##################################################################################


def add_to_cart(request, isbn):
    if request.user.is_authenticated:
        try:
            book = Books.objects.get(pk=isbn)
        except ObjectDoesNotExist:
            pass
        else:
            try:
                cart = Cart.objects.get(user=request.user, active=True)
            except ObjectDoesNotExist:
                cart = Cart.objects.create(user=request.user)
                cart.save()
            cart.add_to_cart(isbn)
        return redirect('CartApp:cartHomeView')
    else:
        return redirect('homeView')


def remove_from_cart(request, isbn):
    if request.user.is_authenticated:
        try:
            book = Books.objects.get(pk=isbn)
        except ObjectDoesNotExist:
            pass
        else:
            cart = Cart.objects.get(user=request.user, active=True)
            cart.remove_from_cart(isbn)
        return redirect('CartApp:cartHomeView')
    else:
        return redirect('homeView')


def cartHomeView(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user.id, active=True)
        except ObjectDoesNotExist:
            # returning an empty list of context
            return render(request, 'CartApp/home.html', {})

        orders = BookOrder.objects.filter(cart=cart)
            
        total = 0
        count = 0
        for order in orders:
            total += (order.book.price * order.quantity)
            count += order.quantity
        context = {
            'cart' : cart,
            'cartItems': orders,
            'total': total,
            'count': count,
        }
        return render(request, 'CartApp/home.html', context)
    else:
        return redirect('homeView')


def checkout(request, cart_id):
    if request.user.is_authenticated:
        # cart = Cart.objects.filter(user=request.user.id, active=True)
        cart = Cart.objects.get(pk=cart_id)
        # cart.active = False
        # cart.save()
        orders = BookOrder.objects.filter(cart=cart_id)
        default_address = cart.user.user.get_full_address()

        address_form = NewAddressForm()
        card_form = CardForm()
        return render(request, 'CartApp/checkout.html', {'address_form':address_form, 'address':default_address, 'card_form':card_form})
    else:
        return redirect('homeView')

def orderPlacedView(request):
    return render(request, "CartApp/orderplaced.html", {})