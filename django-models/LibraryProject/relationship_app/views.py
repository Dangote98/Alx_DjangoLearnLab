from typing import Any
from django.shortcuts import render
from django.views.generic import DetailView,TemplateView,ListView
from .models import Librarian,Library,Author,Book
# Create your views here.

def book_detail_view (request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request,'relationship_app/list_books.html',context)

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    pk_url_kwarg = 'id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
# Create your views here.
