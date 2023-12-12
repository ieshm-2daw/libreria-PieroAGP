from datetime import date
from typing import Any
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View

from .models import Libro,Autor,Prestamo


from django.views.generic import ListView, CreateView ,DetailView, UpdateView, DeleteView
# Create your views here.

class BookListView(ListView):
    model = Libro
    template_name='book/lista_libros.html'
    #pintar por un lado libro disponibles y no disponibles
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        #sacar dos datos del contexto
        context= super().get_context_data(**kwargs)
        context['libros_disponibles'] = Libro.objects.filter(disponibilidad="disponible")
        context["libros_prestados"] = Libro.objects.filter(disponibilidad="prestado")

        return context

    #queryset=Libro.objects.filter(disponibilidad="disponible")
    

"""
class NuevoAutor(CreateView):
    model = Autor
    fields = ["nombre_autor","biografia","foto"]
    template_name = 'book/nuevo_autor.html'
    success_url = 'lista_libros'
"""

class NuevoLibro(CreateView):
    model = Libro
    fields = ["titulo","autores","editorial","fecha_publicacion","genero","isbn","resumen","portada","disponibilidad"]
    template_name = 'book/nuevo_libro.html'
    success_url = reverse_lazy('lista_libros')

class DetalleLibro(DetailView):
    model = Libro
    template_name = 'book/detalle_libro.html'

class EditarLibro(UpdateView):
    model = Libro
    fields = ["titulo","autores","editorial","fecha_publicacion","genero","isbn","resumen","portada","disponibilidad"]
    template_name = "book/editar_libro.html" 
    success_url= reverse_lazy('lista_libros')

class EliminarLibro(DeleteView):
    model = Libro
    success_url = reverse_lazy('lista_libros')
    template_name="book/eliminar_libro.html"

#INtentar prestamo con clase
"""
class PrestamoLibro(View):
    libro = get_object_or_404(Libro,pk=pk)
    def get(self,request):
        return render(request,'book/prestamo_libro.html',{'libro':libro})
"""   

def prestamo_libro(request, pk):
    libro = get_object_or_404(Libro,pk=pk)

    if request.method == 'POST':
        
        fecha_prestamo = date.today()
        fecha_devolucion = date.today()
        #
        Prestamo.objects.create(
            libro = libro,
            fecha_prestamo = fecha_prestamo,
            fecha_devolucion = fecha_devolucion,
            usuario = request.user,
            estado = 'prestado' 
        )
        libro.disponibilidad='prestado'
        libro.save()

        return redirect('detalle_libro',pk=pk)
#get
    return render(request,'book/prestamo_libro.html',{'libro':libro})