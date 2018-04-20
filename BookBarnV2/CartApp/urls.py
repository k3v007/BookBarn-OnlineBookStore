from django.urls import path, re_path
from django.urls import reverse
from .import views

app_name='CartApp'

urlpatterns = [
	re_path(r'^$', views.cartHomeView, name='cartHomeView'),
	re_path(r'^add/(?P<isbn>\w+)/$', views.add_to_cart, name='add_to_cart'),
	re_path(r'^remove/(?P<isbn>\w+)/$', views.remove_from_cart, name='remove_from_cart'),
	re_path(r'^checkout/(?P<cart_id>\d+)/$', views.checkout, name='checkout'),
	re_path(r'^orderplaced/$', views.orderPlacedView, name='orderPlacedView'),
	# re_path(r'^update/$', views.cartUpdateView, name='cartUpdateView')
]