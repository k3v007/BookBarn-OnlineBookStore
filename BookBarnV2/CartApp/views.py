from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Cart, BookOrder
from .forms import AddressChoiceForm, NewAddressForm, CardForm
from BookBarnApp.models import Books

# Create your views here.

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


#####################################
# Not working properly :(

def checkout(request, cart_id):
    if request.user.is_authenticated:
        # cart = Cart.objects.filter(user=request.user.id, active=True)
        cart = Cart.objects.get(pk=cart_id)
        # cart.active = False
        # cart.save()
        orders = BookOrder.objects.filter(cart=cart_id)
        default_address = cart.user.user.get_full_address()

        if request.method == 'POST':
            pwd_form = AddressChoiceForm(data=request.POST)
            # print('\n\n')
            # print(pwd_form)
            # print('\n\n')
            if pwd_form.is_valid():                
                pwd_form.save()                
            else:
                print(pwd_form.errors)

       ############## 
        address_form = NewAddressForm()
        card_form = CardForm()
        return render(request, 'CartApp/checkout.html', {'address_form':address_form, 'address':default_address, 'card_form':card_form, 'cart':cart})
    else:
        return redirect('homeView')

#####################################

def orderPlacedView(request):
    return render(request, "CartApp/orderplaced.html", {})