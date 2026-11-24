from django.db import models
from django.contrib.auth.models import User
from administrador.models import ComplejoCancha, PerfilHost

class Partido(models.Model):
    MODALIDAD_CHOICES = [
        ('F5', 'Fútbol 5'),
        ('F7', 'Fútbol 7'),
        ('F8', 'Fútbol 8'),
        ('F11', 'Fútbol 11'),
    ]

    SUPERFICIE_CHOICES = [
        ('Césped Sintético', 'Césped Sintético'),
        ('Césped Natural', 'Césped Natural'),
        ('Parquet Flotante', 'Parquet Flotante'),
        ('Cemento', 'Cemento'),
    ]

    titulo = models.CharField(max_length=150)
    creador = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='partidos_propios')
    complejo = models.ForeignKey(ComplejoCancha, on_delete=models.SET_NULL, null=True, blank=True)
    
    modalidad = models.CharField(max_length=5, choices=MODALIDAD_CHOICES, default='F7')
    es_mixto = models.BooleanField(default=False)
    nivel = models.CharField(max_length=50, default='Intermedio')
    zona = models.CharField(max_length=100, default='Zona Oeste / Rafael Castillo')
    
    jugadores_totales = models.IntegerField(default=14)
    jugadores_faltantes = models.IntegerField(default=2)
    fecha_partido = models.DateTimeField(null=True, blank=True)
    hora_formato = models.CharField(max_length=20, default='21:00 hs')
    fecha_formato = models.CharField(max_length=30, default='Hoy')
    
    cancha_nombre = models.CharField(max_length=150, default='Complejo Deportivo')
    cancha_direccion = models.CharField(max_length=250, default='Rafael Castillo')
    superficie = models.CharField(max_length=30, choices=SUPERFICIE_CHOICES, default='Césped Sintético')
    precio_por_jugador = models.DecimalField(max_digits=8, decimal_places=2, default=3500.00)
    descripcion = models.TextField(blank=True, null=True)
    distancia_km = models.FloatField(default=1.2)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.modalidad} ({self.cancha_nombre})"

class SolicitudUnirse(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada'),
    ]

    partido = models.ForeignKey(Partido, on_delete=models.CASCADE, related_name='solicitudes')
    jugador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    nombre_jugador = models.CharField(max_length=100)
    posicion = models.CharField(max_length=30, default='Mediocampista')
    nivel = models.CharField(max_length=30, default='Intermedio')
    telefono = models.CharField(max_length=30, default='+54 9 11 0000-0000')
    mensaje = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Postulación de {self.nombre_jugador} para {self.partido.titulo}"

class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensaje de {self.nombre} ({self.email})"