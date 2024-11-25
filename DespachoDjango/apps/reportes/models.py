from django.db import models

class Reporte(models.Model):
    nombre = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre
