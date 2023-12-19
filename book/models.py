from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class Autor(models.Model):
    nombre_autor= models.CharField(max_length=100)
    biografia = models.TextField()
    foto = models.ImageField(upload_to='autores/',null=True, blank=True)

    def __str__(self):
        return self.nombre_autor

class Editorial(models.Model):
    nombre=models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    sitio_web = models.URLField()

    def __str__(self):
        return self.nombre

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autores = models.ManyToManyField(Autor)
    editorial = models.ForeignKey("Editorial", on_delete=models.CASCADE)
    valoracion_libro = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    fecha_publicacion = models.DateField()
    genero = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13)
    resumen = models.TextField()
    portada = models.ImageField(upload_to='portadas/', null=True, blank=True)

    DISPONIBILIDAD_CHOICES = (
        ('disponible', 'Disponible'),
        ('prestado','Prestado'),
        ('en_proceso', 'En proceso de préstamo'),
    )

    disponibilidad = models.CharField(max_length=20, choices=DISPONIBILIDAD_CHOICES, default='disponible')
    created_at= models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo

class Usuario(AbstractUser):
    dni = models.CharField(max_length=10, unique=False)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15)
    
    def __str__(self):
        return self.username

class Prestamo(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    fecha_prestamo = models.DateField()
    fecha_devolucion = models.DateField(null=True, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    ESTADO_CHOICES = (
        ('prestado','Prestado'),
        ('devuelto', 'Devuelto'),
    )
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='prestado')

    def __str__(self):
        return f"Prestado de {self.libro.titulo} a {self.usuario}"


class Valoracion(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    #campo de valoracion
    valoracion_por_usuario = models.DecimalField(max_digits=2, decimal_places=1,validators=[MinValueValidator(0),MaxValueValidator(5)])

    def __str__(self):
        return f"Valoracion de {self.libro.titulo} a {self.usuario}"
    