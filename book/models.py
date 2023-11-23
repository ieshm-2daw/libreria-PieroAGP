from django.db import models

# Create your models here.

class Usuario(models.Model):
    dni = models.CharField(max_length=200)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=200)

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    nombre_autor = models.CharField(max_length=200)
    editorial = models.CharField(max_length=200)
    fecha_publicacion = models.DateField()
    genero = models.CharField(max_length=200)
    isbn = models.CharField(max_length=200)
    resumen = models.TextField()
    disponible = models.CharField(max_length=200)
    portada = models.CharField(max_length=200)

class Author(models.Model):
    nombre_autor= models.CharField(max_length=200)
    biografia = models.TextField()
    foto = models.CharField(max_length=200)

class Prestamo():
    libro_prestado = models.CharField(max_length=200)
    fecha_prestamo = models.DateField()
    fecha_devolucion = models.DateField()
    usuario = models.CharField(max_length=200)
    estado = models.CharField(max_length=200)
    