from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cliente.models import Partido, SolicitudUnirse
from .models import ComplejoCancha, PerfilHost
from django.contrib import messages

@login_required
def index_administrador(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        jugadores_faltantes = request.POST.get('jugadores_faltantes')
        fecha_partido = request.POST.get('fecha_partido')
        es_mixto = True if request.POST.get('es_mixto') == 'on' else False
        nivel = request.POST.get('nivel', 'Intermedio')
        zona = request.POST.get('zona', 'Zona Oeste / Rafael Castillo')
        
        cancha_nombre = request.POST.get('nombre_estadio') or request.POST.get('cancha_nombre', 'Complejo Deportivo')
        cancha_direccion = request.POST.get('direccion') or request.POST.get('cancha_direccion', 'Rafael Castillo')
        
        if titulo:
            Partido.objects.create(
                titulo=titulo,
                jugadores_faltantes=int(jugadores_faltantes) if jugadores_faltantes else 2,
                es_mixto=es_mixto,
                nivel=nivel,
                zona=zona,
                cancha_nombre=cancha_nombre,
                cancha_direccion=cancha_direccion,
                creador=request.user
            )
        return redirect('index_administrador')

    partidos = Partido.objects.filter(creador=request.user).order_by('-id')
    solicitudes_pendientes = SolicitudUnirse.objects.filter(partido__creador=request.user, estado='Pendiente')
    
    contexto = {
        'partidos': partidos,
        'solicitudes_pendientes': solicitudes_pendientes
    }
    return render(request, 'administrador/index.html', contexto)

@login_required
def eliminar_partido(request, partido_id):
    partido = get_object_or_404(Partido, id=partido_id, creador=request.user)
    partido.delete()
    return redirect('index_administrador')

@login_required
def aceptar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudUnirse, id=solicitud_id, partido__creador=request.user)
    solicitud.estado = 'Aceptada'
    solicitud.save()
    
    partido = solicitud.partido
    if partido.jugadores_faltantes > 0:
        partido.jugadores_faltantes -= 1
        partido.save()
        
    return redirect('index_administrador')

@login_required
def rechazar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudUnirse, id=solicitud_id, partido__creador=request.user)
    solicitud.estado = 'Rechazada'
    solicitud.save()
    return redirect('index_administrador')

@login_required
def detalle_partido_host(request, partido_id):
    partido = get_object_or_404(Partido, id=partido_id, creador=request.user)
    jugadores_confirmados = SolicitudUnirse.objects.filter(partido=partido, estado='Aceptada')
    solicitudes_pendientes = SolicitudUnirse.objects.filter(partido=partido, estado='Pendiente')
    
    contexto = {
        'partido': partido,
        'jugadores_confirmados': jugadores_confirmados,
        'solicitudes_pendientes': solicitudes_pendientes,
    }
    return render(request, 'administrador/detalle_partido.html', contexto)

def dashboard_admin(request):
    complejos = ComplejoCancha.objects.all()
    hosts = PerfilHost.objects.all()
    context = {
        'complejos': complejos,
        'hosts': hosts,
    }
    return render(request, 'administrador/dashboard.html', context)

def registrar_complejo(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        direccion = request.POST.get('direccion')
        zona = request.POST.get('zona', 'Zona Oeste / Rafael Castillo')
        superficies = request.POST.get('superficies', 'Césped Sintético')
        telefono = request.POST.get('telefono')

        ComplejoCancha.objects.create(
            nombre=nombre,
            direccion=direccion,
            zona=zona,
            superficies_disponibles=superficies,
            telefono_contacto=telefono
        )
        messages.success(request, "¡Complejo deportivo registrado con éxito! 🏟️")
        return redirect('dashboard_admin')
    
    return render(request, 'administrador/registrar_complejo.html')