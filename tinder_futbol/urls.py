from django.contrib import admin
from django.urls import path, include
from cliente.views import login_usuario

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_usuario, name='login'),  # <-- La raíz ahora muestra el login directamente
    path('accounts/', include('allauth.urls')),
    path('cliente/', include('cliente.urls')),
]