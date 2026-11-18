from django.db import models

class ComplejoCancha(models.Model):
    nombre = models.CharField(max_length=150)
    direccion = models.CharField(max_length=250)
    zona = models.CharField(max_length=100, default='Zona Oeste / Rafael Castillo')
    superficies_disponibles = models.CharField(max_length=150, help_text="Ej: Césped Sintético, Césped Natural")
    telefono_contacto = models.CharField(max_length=30)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.zona})"

class PerfilHost(models.Model):
    nombre_completo = models.CharField(max_length=100)
    telefono = models.CharField(max_length=30)
    calificacion_promedio = models.FloatField(default=5.0)
    partidos_organizados_total = models.IntegerField(default=0)
    verificado = models.BooleanField(default=True)

    def __str__(self):
        return f"Host: {self.nombre_completo} (★ {self.calificacion_promedio})"