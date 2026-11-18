from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_administrador, name='index_administrador'),
    path('aceptar/<int:solicitud_id>/', views.aceptar_solicitud, name='aceptar_solicitud'),
    path('rechazar/<int:solicitud_id>/', views.rechazar_solicitud, name='rechazar_solicitud'),
    path('eliminar/<int:partido_id>/', views.eliminar_partido, name='eliminar_partido'),
    path('partido/<int:partido_id>/', views.detalle_partido_host, name='detalle_partido_host'),
    path('dashboard/', views.dashboard_admin, name='dashboard_admin'),
    path('complejo/nuevo/', views.registrar_complejo, name='registrar_complejo'),
]