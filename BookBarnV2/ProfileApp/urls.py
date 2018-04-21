from django.urls import path, re_path
from django.urls import reverse
from .import views

app_name='ProfileApp'

urlpatterns = [
	re_path(r'^$', views.profileView, name='profileView'),
	re_path(r'^update/$', views.updateProfileView, name='updateProfileView'),
	re_path(r'^pwd_reset/$', views.updatePasswordView, name='updatePasswordView'),
	re_path(r'^order_history/$', views.orderHistoryView, name='orderHistoryView'),
	re_path(r'^order_history/(?P<order_id>\d+)/$', views.orderDetailsView, name='orderDetailsView'),
]