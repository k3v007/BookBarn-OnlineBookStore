from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from BookBarnApp.models import Authors, Books, Publishers, Genres, UserProfiles
from datetime import date, datetime, timedelta
from ProfileApp.forms import UserUpdateForm, UserProfileUpdateForm, UserPwdUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from CartApp.models import Cart, BookOrder
from django.forms.models import model_to_dict

# Create your views here.
app_name = 'ProfileApp'

def profileView(request):
    return render(request, 'ProfileApp/profile.html', {})

def updateProfileView(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(data=request.POST, instance=request.user)
        profile_form = UserProfileUpdateForm(data=request.POST, instance=request.user.user)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()            
            return render(request, 'ProfileApp/profile.html', {'message': "<-- Profile updated successfully -->"})
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user = User.objects.get(username = request.user.username)
        user_profile = UserProfiles.objects.filter(user=request.user).first() 
        user_form = UserUpdateForm(initial=model_to_dict(user))
        profile_form = UserProfileUpdateForm(initial=model_to_dict(user_profile))

    return render(request, 'ProfileApp/update.html', {'user_form': user_form, 'profile_form': profile_form})


def updatePasswordView(request):
    if request.method == 'POST':
        pwd_form = UserPwdUpdateForm(data=request.POST, instance=request.user)

        if pwd_form.is_valid():
            user = pwd_form.save()
            user.set_password(user.password)
            user.save()
            return render(request, 'ProfileApp/profile.html', {'message': "<-- Password reset successfully -->"})
        else:
            print(pwd_form.errors)
    else:
        pwd_form = UserPwdUpdateForm()

    return render(request, 'ProfileApp/pwd_reset.html', {'pwd_form': pwd_form})


def orderHistoryView(request):
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user.id, active=False)
        return render(request, 'ProfileApp/order_history.html', {'carts':carts})
    else:
        return redirect('homeView')



def orderDetailsView(request, order_id):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(pk=order_id)
        except ObjectDoesNotExist:
            # returning an empty list of context
            return render(request, 'ProfileApp/home.html', {})
        orders = BookOrder.objects.filter(cart=cart)
        return render(request, 'ProfileApp/order_details.html', {'orders':orders, 'order_id':order_id})
    else:
        return redirect('homeView')