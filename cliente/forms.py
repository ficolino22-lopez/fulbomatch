from django import forms
from .models import MensajeContacto

class ContactoForm(forms.ModelForm):
    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'email', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-xs text-slate-100 focus:outline-none focus:border-primary', 'placeholder': 'Tu nombre'}),
            'email': forms.EmailInput(attrs={'class': 'w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-xs text-slate-100 focus:outline-none focus:border-primary', 'placeholder': 'tu@email.com'}),
            'mensaje': forms.Textarea(attrs={'class': 'w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-xs text-slate-100 focus:outline-none focus:border-primary', 'rows': 4, 'placeholder': 'Escribe tu consulta aquí...'}),
        }