from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from BookBarnApp.models import Authors, Books, Publishers, Genres, UserProfiles
from datetime import date, datetime, timedelta
from BookBarnApp.forms import UserSignupForm, UserProfileSignupForm, LoginForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from CartApp.models import Cart
# from django.db import connection

# Create your views here.


# def my_custom_sql(word):
#     with connection.cursor() as cursor:
#         cursor.execute("select BookTitle, coverImage, isbn from books as b join books_genres as bg on b.isbn = bg.book_isbn join genres as g on bg.genre_gid = g.gid where gName = " + word + " order by rating desc limit 6")
#         row = cursor.fetchall()
#     return row;

#Template Tagging
app_name = 'BookBarnApp'

# To show home page
def homeView(request):
    trending = Books.objects.order_by('-rating')[:6]
    fiction = Genres.objects.get(gName='Fiction').books.all()[:6]
    thriller = Genres.objects.get(gName='Thriller').books.all()[:6]
    drama = Genres.objects.get(gName='Drama').books.all()[:6]
    romance = Genres.objects.get(gName='Romance').books.all()[:6]
    mystery = Genres.objects.get(gName='Mystery').books.all()[:6]
    scific = Genres.objects.get(gName='Science Fiction').books.all()[:6]
    books_dict = {'trending':trending, 'fiction':fiction, 'thriller':thriller, 'drama':drama, 'romance':romance, 'mystery':mystery, 'scific':scific}
    return render(request, 'BookBarnApp/home.html', context=books_dict)

# To show a single book's details
def bookView(request, isbn):
    book = get_object_or_404(Books, pk=isbn)
    # cart_obj, new_obj = Cart.objects.new_or_get(request)
    # context = {'book':book, 'genre':'', 'cart': cart_obj}
    rating_percent = (book.rating / 5) * 100
    context = {'book':book, 'rating_percent':rating_percent}
    return render(request, 'BookBarnApp/book.html', context)

# To show books in a single category
def categoryView(request, gid):
    # genre = get_object_or_404(Genres, pk=gid)
    books_list = Genres.objects.get(gid=gid).books.all()
    paginator = Paginator(books_list, 15) # Show 20 books list per page
    page = request.GET.get('page')
    books = paginator.get_page(page)
    return render(request, 'BookBarnApp/category.html', {'books':books})

# To show list of categories
def categoryListView(request):
    genres = Genres.objects.all()
    paginator = Paginator(genres, 20) # Show 20 genres list per page
    page = request.GET.get('page')
    genres_list = paginator.get_page(page)
    return render(request, 'BookBarnApp/categorylist.html', {'categories':genres_list})


# For signup/register
def signupView(request):
    registered = False
    if request.method == 'POST':
        user_form = UserSignupForm(data=request.POST)
        profile_form = UserProfileSignupForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserSignupForm()
        profile_form = UserProfileSignupForm()

    return render(request, 'BookBarnApp/signup.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

# For logging in
def loginView(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('homeView'))
            else:
                return HttpResponse("Your BookBarn account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        form = LoginForm()
        context = { 'form':form }
        return render(request, 'BookBarnApp/login.html', context)

# For logging out
@login_required
def logoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse('homeView'))

