from django.urls import path, re_path
from django.urls import reverse
from .import views

app_name='SearchApp'

urlpatterns = [
	re_path(r'^search/$', views.SearchBookView.as_view(), name='SearchBookView'),
]