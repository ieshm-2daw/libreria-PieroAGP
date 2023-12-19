from django.urls import path, include
from . import views
from .views import *

urlpatterns = [
    path('', BookListView.as_view(), name='lista_libros'),
    path('book/nuevoLibro/', NuevoLibro.as_view(), name='nuevo_libro'),
    path('book/nuevoAutor/', NuevoAutor.as_view(), name='nuevo_autor'),
    path('book/detalleLibro/<int:pk>', DetalleLibro.as_view(), name='detalle_libro'),
    path('book/<int:pk>/edit', EditarLibro.as_view(),name='editar_libro'),
    path('book/<int:pk>/delete',EliminarLibro.as_view(),name='elimninar_libro'),
    path('book/<int:pk>/prestamo',views.prestamo_libro,name='prestamo_libro'),
    path('book/<int:pk>/devolver',views.devolver_libro,name='devolver_libro'),
    path('book/mis_libros', ListadoUsuarioLibros.as_view(), name='mis_libros'),
    path('book/<int:pk>/valoracion',views.valoracion_usuario_libro,name='valoracion_libro'),
]