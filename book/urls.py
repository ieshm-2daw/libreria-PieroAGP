from django.urls import path, include
from . import views
from .views import *

urlpatterns = [
    path('', BookListView.as_view(), name='lista_libros'),
    path('book/nuevoLibro/', NuevoLibro.as_view(), name='nuevo_libro'),
    path('book/detalleLibro/<int:pk>', DetalleLibro.as_view(), name='detalle_libro')
]