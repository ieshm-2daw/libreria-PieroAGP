from datetime import date
from typing import Any
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View

from .models import Libro,Autor,Prestamo,Valoracion

from django.contrib.auth.decorators import login_required

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


class ListadoUsuarioLibros(ListView):
    model = Prestamo
    template_name = 'book/mis_libros.html'
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context= super().get_context_data(**kwargs)
        context["prestamos_prestados"] = Prestamo.objects.filter(estado="prestado",usuario=self.request.user)
        context["prestamos_devueltos"] = Prestamo.objects.filter(estado="devuelto",usuario=self.request.user)

        return context


class NuevoAutor(CreateView):
    model = Autor
    fields = ["nombre_autor","biografia","foto"]
    template_name = 'book/nuevo_autor.html'
    success_url = reverse_lazy('lista_libros')


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

@login_required
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

        return redirect('lista_libros')
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

        return redirect('valoracion_libro', pk=pk)
    
    return render(request,'book/devolver_libro.html',{'libro':v_libro})

def valoracion_usuario_libro(request, pk):
    v_libro = get_object_or_404(Libro, pk=pk)
    #con get_object_or_404 no funciona el firts
    #v_prestamo = get_object_or_404(Prestamo,libro = v_libro,usuario = request.user).first()

    #usando filter me da muchos prestamos de ese libro por ese usuario, con firts solo me quedo con el primero
    v_prestamo = Prestamo.objects.filter(libro=v_libro, usuario = request.user).first() 
    
    if request.method == 'POST':
        #para quedamre con la valoracion del usuario
        nueva_valoracion = float(request.POST['valoracion'])
        try:
            v_valoracion=Valoracion.objects.get(libro=v_libro,usuario=v_prestamo.usuario)
        except Valoracion.DoesNotExist:
            v_valoracion= None
        
        if v_valoracion is None:
            Valoracion.objects.create(
                libro=v_libro,
                usuario = v_prestamo.usuario,
                valoracion_por_usuario=nueva_valoracion,
            )
        else:
            v_valoracion.valoracion_por_usuario=nueva_valoracion
            v_valoracion.save()

        #recorremos la tabla de valoracion por el libro devuelto y calculamos su media
        t_valoracion = Valoracion.objects.all()
        num_valoraciones = len(Valoracion.objects.filter(libro=v_libro))
        acumulador_valoracion = 0
        for valoracion in t_valoracion:
            if valoracion.libro.titulo == v_libro.titulo:
                acumulador_valoracion += valoracion.valoracion_por_usuario
        media_valoracion=(acumulador_valoracion/num_valoraciones)

        #actualizamos la valoracion del Libro
        v_libro.valoracion_libro = media_valoracion
        v_libro.save()

        return redirect('lista_libros')
    
    return render(request, 'book/valoracion_libro.html',{'libro':v_libro})