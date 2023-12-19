from django.contrib import admin
from .models import Usuario, Autor, Editorial, Libro, Prestamo, Valoracion

# Register your models here.

admin.site.register(Usuario)
admin.site.register(Autor)
admin.site.register(Editorial)
admin.site.register(Libro)
admin.site.register(Prestamo)
admin.site.register(Valoracion)
