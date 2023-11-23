from django.urls import path, include
from . import views
from .views import *

urlpatterns = [
    path('', BookListView.as_view(), name='lista_libros'),
    
]