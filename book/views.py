from django.shortcuts import render
from django.urls import reverse_lazy

from .models import Libro,Autor


from django.views.generic import ListView, CreateView ,DetailView
# Create your views here.

class BookListView(ListView):
    model = Libro
    template_name='book/lista_libros.html'
"""
class NuevoAutor(CreateView):
    model = Autor
    fields = ["nombre_autor","biografia","foto"]
    template_name = 'book/nuevo_autor.html'
    success_url = 'lista_libros'
"""

class NuevoLibro(CreateView):
    model = Libro
    fields = ["titulo","autores","editorial","fecha_publicacion","genero","isbn","resumen","portada"]
    template_name = 'book/nuevo_libro.html'
    success_url = reverse_lazy('lista_libros')

class DetalleLibro(DetailView):
    model = Libro
    template_name = 'book/detalle_libro.html'