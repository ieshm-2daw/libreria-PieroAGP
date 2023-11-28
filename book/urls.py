from django.urls import path, include
from . import views
from .views import *

urlpatterns = [
    path('', BookListView.as_view(), name='lista_libros'),
    path('book/nuevoLibro/', NuevoLibro.as_view(), name='nuevo_libro'),
    path('book/detalleLibro/<int:pk>', DetalleLibro.as_view(), name='detalle_libro'),
    path('book/<int:pk>/edit', EditarLibro.as_view(),name='editar_libro'),
    path('book/<int:pk>/delete',EliminarLibro.as_view(),name='elimninar_libro')
]