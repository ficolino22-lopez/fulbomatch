from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Partido, SolicitudUnirse
from .forms import ContactoForm
from .models import MensajeContacto
from django.core.paginator import Paginator
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string




def bienvenida_view(request):
    return render(request, 'cliente/bienvenida.html')

def registro_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect('seleccion_perfil')
    else:
        form = UserCreationForm()
    return render(request, 'cliente/registro.html', {'form': form})

def login_usuario(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('seleccion_perfil') 
    else:
        form = AuthenticationForm()
    return render(request, 'cliente/login.html', {'form': form})

@login_required(login_url='login')
def seleccion_perfil(request):
    return render(request, 'cliente/seleccion_perfil.html')

def logout_usuario(request):
    logout(request)
    return redirect('bienvenida')

def index_cliente(request):
    # Limpiar y filtrar mensajes duplicados de la sesión
    storage = messages.get_messages(request)
    seen = set()
    mensajes_unicos = []
    for m in storage:
        if m.message not in seen:
            seen.add(m.message)
            mensajes_unicos.append(m)

    zona_seleccionada = request.GET.get('zona', None)
    
    if zona_seleccionada:
        partidos = Partido.objects.filter(zona=zona_seleccionada, activo=True).order_by('-id')
    else:
        partidos = Partido.objects.filter(activo=True).order_by('-id')
    
    zonas_disponibles = Partido.objects.values_list('zona', flat=True).distinct()
    zonas = [z for z in zonas_disponibles if z]

    contexto = {
        'partidos': partidos,
        'zonas': zonas,
        'zona_seleccionada': zona_seleccionada,
        'mensajes_unicos': mensajes_unicos,  # <-- Pasamos los mensajes filtrados
    }
    return render(request, 'cliente/index.html', contexto)

@login_required
def unirse_partido(request, partido_id):
    partido = get_object_or_404(Partido, id=partido_id)
    
    SolicitudUnirse.objects.get_or_create(
        partido=partido,
        jugador=request.user,
        defaults={
            'nombre_jugador': request.user.first_name or request.user.username,
            'estado': 'pendiente'
        }
    )
    messages.success(request, "¡Te postulaste con éxito! El host revisará tu solicitud.")
    return redirect('index_cliente')

@login_required
def crear_partido(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        modalidad = request.POST.get('modalidad', 'F7')
        nivel = request.POST.get('nivel', 'Intermedio')
        superficie = request.POST.get('superficie', 'Césped Sintético')
        jugadores_faltantes = request.POST.get('jugadores_faltantes', 2)
        es_mixto = True if request.POST.get('es_mixto') == 'on' else False
        zona = request.POST.get('zona', 'Zona Oeste / Rafael Castillo')
        cancha_nombre = request.POST.get('cancha_nombre', 'Complejo Deportivo')
        precio = request.POST.get('precio_por_jugador', 3500.00)
        
        Partido.objects.create(
            titulo=titulo,
            modalidad=modalidad,
            nivel=nivel,
            superficie=superficie,
            jugadores_faltantes=int(jugadores_faltantes) if jugadores_faltantes else 2,
            es_mixto=es_mixto,
            zona=zona,
            cancha_nombre=cancha_nombre,
            precio_por_jugador=precio,
            creador=request.user
        )
        messages.success(request, "¡Partido publicado en el Mazo con éxito!")
        return redirect('index_cliente')
        
    return render(request, 'cliente/crear_partido.html')

@login_required
def panel_host(request):
    mis_partidos = Partido.objects.filter(creador=request.user, activo=True)
    solicitudes = SolicitudUnirse.objects.filter(partido__creador=request.user, estado='pendiente')
    
    contexto = {
        'mis_partidos': mis_partidos,
        'solicitudes': solicitudes,
    }
    return render(request, 'cliente/panel_host.html', contexto)

@login_required
def aceptar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudUnirse, id=solicitud_id, partido__creador=request.user)
    solicitud.estado = 'aceptada'
    solicitud.save()
    
    partido = solicitud.partido
    if partido.jugadores_faltantes > 0:
        partido.jugadores_faltantes -= 1
        partido.save()
        
    messages.success(request, f"¡Aceptaste a {solicitud.nombre_jugador} en el equipo!")
    return redirect('panel_host')

@login_required
def rechazar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudUnirse, id=solicitud_id, partido__creador=request.user)
    solicitud.estado = 'rechazada'
    solicitud.save()
    return redirect('panel_host')

@login_required(login_url='login')
def mis_solicitudes(request):
    solicitudes = SolicitudUnirse.objects.filter(jugador=request.user).order_by('-fecha_creacion')
    return render(request, 'cliente/mis_solicitudes.html', {'solicitudes': solicitudes})

def politica_privacidad(request):
    return render(request, 'cliente/politica_privacidad.html')

def terminos_condiciones(request):
    return render(request, 'cliente/terminos_condiciones.html')

def contacto_view(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            contacto = form.save()
            
            # 1. Correo HTML al Administrador (Doble envío requerido)
            try:
                asunto_admin = f"Nuevo mensaje de contacto de {contacto.nombre}"
                html_mensaje = render_to_string('cliente/email_template.html', {'contacto': contacto})
                email_admin = EmailMessage(
                    asunto_admin,
                    html_mensaje,
                    'tu_correo@gmail.com',
                    ['tu_correo@gmail.com'],
                )
                email_admin.content_subtype = 'html'
                email_admin.send(fail_silently=True)

                # 2. Acuse de recibo automático al cliente
                send_mail(
                    'Hemos recibido tu consulta - Fulbo Match',
                    f'Hola {contacto.nombre},\n\nHemos recibido tu mensaje y nos pondremos en contacto a la brevedad.\n\nAtentamente,\nEl equipo de Fulbo Match.',
                    'tu_correo@gmail.com',
                    [contacto.email],
                    fail_silently=True,
                )
            except Exception as e:
                print("Error al enviar correo: ", e)

            messages.success(request, "¡Mensaje enviado con éxito! Te responderemos pronto.")
            return redirect('gracias')
    else:
        form = ContactoForm()
    return render(request, 'cliente/contacto.html', {'form': form})

def gracias_view(request):
    return render(request, 'cliente/gracias.html')

@login_required
def listar_mensajes(request):
    # Validar que sea usuario administrador / staff
    if not request.user.is_staff:
        return redirect('index_client')
    
    mensajes_list = MensajeContacto.objects.all().order_by('-fecha_envio')
    paginator = Paginator(mensajes_list, 5) # 5 mensajes por página (Requerido)
    page_number = request.GET.get('page')
    mensajes = paginator.get_page(page_number)
    
    return render(request, 'cliente/listar_mensajes.html', {'mensajes': mensajes})