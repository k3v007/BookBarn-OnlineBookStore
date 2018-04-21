from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Cart, BookOrder
from .forms import NewAddressForm, CardForm
from BookBarnApp.models import Books
from django.utils import timezone

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
        cart.total = total
        cart.save()
        context = {
            'cart' : cart,
            'cartItems': orders,
            'count': count,
        }
        return render(request, 'CartApp/home.html', context)
    else:
        return redirect('homeView')



def checkout(request, cart_id):
    if request.user.is_authenticated:
        # Getting the active cart of the user, active already handled in cartHomeView
        cart = Cart.objects.get(pk=cart_id)
        
        if cart.active == True:     #To disable the repayment of the same order
            # orders = BookOrder.objects.filter(cart=cart_id)
            default_address = cart.user.user.get_full_address()        
            address_choice = request.POST.get('address')
            payment_choice = request.POST.get('payment')

            if request.method == 'POST':
                if address_choice == 'new_add':
                    new_address_form = NewAddressForm(request.POST)
                    if new_address_form.is_valid():
                        address1 = new_address_form.cleaned_data['address1']               
                        address2 = new_address_form.cleaned_data['address2']
                        city = new_address_form.cleaned_data['city']
                        state = new_address_form.cleaned_data['state']
                        pinCode = new_address_form.cleaned_data['pinCode']
                        address = address1 + ', ' + address2 + '\n' + city + '\n' + state + ' - ' + pinCode
                        # Saving to the model
                        cart.delivery_address = address               
                else:
                    cart.delivery_address = default_address

                if payment_choice == 'card_pay':
                    card_form = CardForm(request.POST)
                    if card_form.is_valid():
                        cart.cardNumber = card_form.cleaned_data['cardNumber']
                        cart.payment_style = 'CARD'
                else:
                    cart.payment_style = 'COD'

                cart.order_date = timezone.now()
                cart.active = False     #Cart payment done, remove it
                cart.save()            
                return render(request, 'CartApp/orderplaced.html', {})
            
            else:
                address_form = NewAddressForm()
                card_form = CardForm()
                return render(request, 'CartApp/checkout.html', {'address_form':address_form, 'address':default_address, 'card_form':card_form, 'cart':cart})
        else:
            return redirect('homeView')
    else:
        return redirect('homeView')



def orderPlacedView(request):
    return render(request, "CartApp/orderplaced.html", {})