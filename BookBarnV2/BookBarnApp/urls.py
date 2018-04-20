from django.urls import path, re_path
from django.urls import reverse
from .import views

urlpatterns = [
	re_path(r'^$', views.homeView, name='homeView'),
	re_path(r'^book/(?P<isbn>\w+)/$', views.bookView, name='bookView'),
	re_path(r'^category/(?P<gid>\w+)/$', views.categoryView, name='categoryView'),
	re_path(r'^signup/$', views.signupView, name='signupView'),
	re_path(r'^login/$', views.loginView, name='loginView'),
	re_path(r'^logout/$', views.logoutView, name='logoutView'),
	re_path(r'^categories/$', views.categoryListView, name='categoryListView')
]