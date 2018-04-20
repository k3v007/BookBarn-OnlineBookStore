from django.urls import path, re_path
from django.urls import reverse
from .import views

app_name='ProfileApp'

urlpatterns = [
	re_path(r'^update/$', views.updateProfileView, name='updateProfileView'),
]