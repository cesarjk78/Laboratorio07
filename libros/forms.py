from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario, Evento, RegistroEvento

# Formulario para registro de usuario
class RegistroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'password1', 'password2']

# Formulario para inicio de sesión
class LoginForm(AuthenticationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'password']

# Formulario para crear un nuevo evento
class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nombre', 'descripcion', 'fecha', 'ubicacion', 'organizador']  # Incluye todos los campos que deseas

# Formulario para registrar un usuario en un evento
class RegistroEventoForm(forms.ModelForm):
    class Meta:
        model = RegistroEvento
        fields = ['usuario', 'evento']  # Asegúrate de incluir los campos que desees para el registro
