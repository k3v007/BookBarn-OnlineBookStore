from django.shortcuts import render
from django.views.generic import ListView
from BookBarnApp.models import Books
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Q

# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
class SearchBookView(ListView):
    template_name = "SearchApp/searchresult.html"

    def get_queryset(self, *args, **kwargs):
        request=self.request;
        query=request.GET.get('q')
        if query is not None:
            lookups=Q(bookTitle__icontains=query) | Q(description__icontains=query)
            return Books.objects.filter(lookups).distinct()
        return Books.objects.none()