from django.shortcuts import render

from .models import Libro


from django.views.generic import ListView, DetailView
# Create your views here.

class BookListView(ListView):
    model = Libro
    template_name='book/lista_libros.html'