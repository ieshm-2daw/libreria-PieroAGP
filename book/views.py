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

class LitaMisLibros(ListView):
    model=Libro
    template_name = 'book/mis_libros.html'
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context= super().get_context_data(**kwargs)
        context["libros_prestados"] = Libro.objects.filter(disponibilidad="prestado")

        return context

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
    v_libro = get_object_or_404(Libro,pk=pk)

    if request.method == 'POST':
        
        fecha_prestamo = date.today()
        fecha_devolucion = date.today()
        #
        Prestamo.objects.create(
            libro = v_libro,
            fecha_prestamo = fecha_prestamo,
            
            usuario = request.user,
            estado = 'prestado' 
        )
        v_libro.disponibilidad='prestado'
        v_libro.save()

        return redirect('detalle_libro',pk=pk)
#get
    return render(request,'book/prestamo_libro.html',{'libro':v_libro})

def devolver_libro(request, pk):
    v_libro = get_object_or_404(Libro, pk=pk)
    prestamo = get_object_or_404(Prestamo,libro = v_libro,usuario = request.user, estado= 'prestado')

    if request.method == 'POST':
        #para el prestamo
        prestamo.estado = 'devuelto'
        prestamo.fecha_devolucion = date.today()
        prestamo.save()

        #para el libro
        v_libro.disponibilidad = 'disponible'
        v_libro.save()

        return redirect('detalle_libro', pk=pk)
    
    return render(request,'book/devolver_libro.html',{'libro':v_libro})