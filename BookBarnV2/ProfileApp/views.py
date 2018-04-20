from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from BookBarnApp.models import Authors, Books, Publishers, Genres, UserProfiles
from datetime import date, datetime, timedelta
from ProfileApp.forms import UserUpdateForm, UserProfileUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from CartApp.models import Cart
from django.forms.models import model_to_dict

# Create your views here.
app_name = 'ProfileApp'

def updateProfileView(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(data=request.POST, instance=request.user)
        profile_form = UserProfileUpdateForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user = User.objects.get(username = request.user.username)
        user_profile = UserProfiles.objects.filter(user=request.user).first() 
        user_form = UserUpdateForm(initial=model_to_dict(user))
        profile_form = UserProfileUpdateForm(initial=model_to_dict(user_profile))

    return render(request, 'ProfileApp/update.html', {'user_form': user_form, 'profile_form': profile_form})