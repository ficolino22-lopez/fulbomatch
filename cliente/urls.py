from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_usuario, name='login'),  # <-- Apunta al login por defecto
    path('bienvenida/', views.bienvenida_view, name='bienvenida'), # Opcional por si quieres conservarla
    path('partidos/', views.index_cliente, name='index_cliente'),
    path('registro/', views.registro_usuario, name='registro_usuario'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    path('seleccion/', views.seleccion_perfil, name='seleccion_perfil'),
    path('crear/', views.crear_partido, name='crear_partido'),
    path('unirse/<int:partido_id>/', views.unirse_partido, name='unirse_partido'),
    path('mis-solicitudes/', views.mis_solicitudes, name='mis_solicitudes'),
    path('panel-host/', views.panel_host, name='panel_host'),
    path('solicitud/aceptar/<int:solicitud_id>/', views.aceptar_solicitud, name='aceptar_solicitud'),
    path('solicitud/rechazar/<int:solicitud_id>/', views.rechazar_solicitud, name='rechazar_solicitud'),
    path('contacto/', views.contacto_view, name='contacto'),
    path('gracias/', views.gracias_view, name='gracias'),
    path('listar-mensajes/', views.listar_mensajes, name='listar_mensajes'),
    path('politica-privacidad/', views.politica_privacidad, name='politica_privacidad'),
    path('terminos-condiciones/', views.terminos_condiciones, name='terminos_condiciones'),
]