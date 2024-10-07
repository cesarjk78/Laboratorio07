from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    fecha_de_registro = models.DateTimeField(auto_now_add=True)

class Evento(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha = models.DateTimeField()
    ubicacion = models.CharField(max_length=255)
    organizador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='eventos_organizados')

    def __str__(self):
        return self.nombre

class RegistroEvento(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='registros')
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='registros')
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'evento')  # Para evitar que un usuario se registre más de una vez en el mismo evento

    def __str__(self):
        return f"{self.usuario.username} en {self.evento.nombre}"
