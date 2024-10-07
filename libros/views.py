from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.db.models import Count
from datetime import datetime
from .models import Usuario, Evento, RegistroEvento
from .forms import EventoForm, RegistroForm, LoginForm

# Lista de eventos
def evento_list(request):
    eventos = Evento.objects.all()
    return render(request, 'libros/libro_list.html', {'eventos': eventos})

# Crear nuevo evento
def evento_create(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('evento_list')  # Redirige a la lista de eventos
    else:
        form = EventoForm()  # Inicializa un formulario vacío para creación
    return render(request, 'libros/libro_form.html', {'form': form})

# Actualizar un evento existente
def evento_update(request, pk):
    evento = get_object_or_404(Evento, pk=pk)  # Busca el evento por su primary key (id)
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('evento_list')  # Redirige a la lista de eventos
    else:
        form = EventoForm(instance=evento)  # Inicializa el formulario con datos del evento existente
    return render(request, 'libros/libro_form.html', {'form': form})

# Eliminar un evento
def evento_delete(request, pk):
    evento = get_object_or_404(Evento, pk=pk)  # Busca el evento por su primary key (id)
    if request.method == 'POST':
        evento.delete()
        return redirect('evento_list')  # Redirige a la lista de eventos después de eliminar
    return render(request, 'libros/libro_confirm_delete.html', {'evento': evento})

# Vista para mostrar eventos y usuarios
def mostrar_eventos_y_usuarios(request):
    eventos = Evento.objects.all()  # Obtener todos los eventos
    usuarios = Usuario.objects.all()  # Obtener todos los usuarios
    return render(request, 'libros/registro_usuario.html', {'eventos': eventos, 'usuarios': usuarios})

# Registrar usuario en un evento
def registrar_usuario(request, evento_pk, usuario_pk):
    evento = get_object_or_404(Evento, pk=evento_pk)  # Busca el evento por su primary key
    usuario = get_object_or_404(Usuario, pk=usuario_pk)  # Busca el usuario por su primary key

    # Verificar si el usuario ya está registrado en el evento
    if RegistroEvento.objects.filter(usuario=usuario, evento=evento).exists():
        return redirect('evento_list')  # Redirigir si ya está registrado

    # Crear el registro en el evento
    RegistroEvento.objects.create(usuario=usuario, evento=evento)
    return redirect('evento_list')  # Redirigir a la lista de eventos después de registrar

# Listar registros de eventos
def registro_evento_list(request):
    registros = RegistroEvento.objects.select_related('usuario', 'evento').all()
    return render(request, 'libros/registro_evento_list.html', {'registros': registros})

# Crear un nuevo registro de evento
def registro_evento_create(request):
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        evento_id = request.POST.get('evento_id')
        usuario = get_object_or_404(Usuario, pk=usuario_id)
        evento = get_object_or_404(Evento, pk=evento_id)

        # Verificar si el usuario ya está registrado
        if RegistroEvento.objects.filter(usuario=usuario, evento=evento).exists():
            return redirect('registro_evento_list')  # Redirigir si ya está registrado

        # Crear el registro en el evento
        RegistroEvento.objects.create(usuario=usuario, evento=evento)
        return redirect('registro_evento_list')  # Redirigir a la lista de registros

    eventos = Evento.objects.all()
    usuarios = Usuario.objects.all()
    return render(request, 'libros/registro_evento_form.html', {'eventos': eventos, 'usuarios': usuarios})

# Actualizar un registro de evento
def registro_evento_update(request, pk):
    registro = get_object_or_404(RegistroEvento, pk=pk)
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        evento_id = request.POST.get('evento_id')
        usuario = get_object_or_404(Usuario, pk=usuario_id)
        evento = get_object_or_404(Evento, pk=evento_id)

        # Actualizar el registro
        registro.usuario = usuario
        registro.evento = evento
        registro.save()
        return redirect('registro_evento_list')

    eventos = Evento.objects.all()
    usuarios = Usuario.objects.all()
    return render(request, 'libros/registro_evento_form.html', {'registro': registro, 'eventos': eventos, 'usuarios': usuarios})

# Eliminar un registro de evento
def registro_evento_delete(request, pk):
    registro = get_object_or_404(RegistroEvento, pk=pk)
    if request.method == 'POST':
        registro.delete()
        return redirect('registro_evento_list')
    return render(request, 'libros/registro_evento_confirm_delete.html', {'registro': registro})

# Vista para mostrar los detalles de un evento
def evento_detail(request, pk):
    evento = get_object_or_404(Evento, pk=pk)  # Obtén el evento por su ID
    return render(request, 'libros/evento_detail.html', {'evento': evento})

def registro_evento_detail(request, pk):
    registro = get_object_or_404(RegistroEvento, pk=pk)  # Obtener el registro por su primary key (pk)
    return render(request, 'libros/registro_evento_detail.html', {'registro': registro})

# Vista para registro de usuario
# Vista para registro de usuario
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            # Iniciar sesión automáticamente después del registro (opcional)
            # login(request, usuario)  # Si no quieres iniciar sesión automáticamente, comenta esta línea
            return redirect('login')  # Redirige al inicio de sesión después del registro
    else:
        form = RegistroForm()  # Inicializa un formulario vacío para registro
    return render(request, 'libros/registro.html', {'form': form})


# Vista para inicio de sesión
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            return redirect('evento_list')  # Aquí puedes redirigir a 'libro_list' o 'evento_list' según lo que necesites
    else:
        form = LoginForm()  # Inicializa un formulario vacío para inicio de sesión
    return render(request, 'libros/login.html', {'form': form})

#orm
def cantidad_usuarios_evento(request, evento_id):
    evento = Evento.objects.get(id=evento_id)
    cantidad_registros = RegistroEvento.objects.filter(evento=evento).count()
    
    context = {
        'evento': evento,
        'cantidad_registros': cantidad_registros,
    }
    return render(request, 'libros/cantidad_usuarios_evento.html', context)

def cantidad_eventos_mes_actual(request):
    hoy = datetime.now()
    mes_actual = hoy.month
    anio_actual = hoy.year

    cantidad_eventos = Evento.objects.filter(fecha__month=mes_actual, fecha__year=anio_actual).count()

    context = {
        'cantidad_eventos': cantidad_eventos,
    }
    return render(request, 'libros/cantidad_eventos_mes.html', context)

def usuarios_mas_activos(request):
    usuarios_activos = (
        Usuario.objects
        .annotate(cantidad_eventos=Count('registros'))  # Cambia 'registroevento' por 'registros'
        .order_by('-cantidad_eventos')
    )

    context = {
        'usuarios_activos': usuarios_activos,
    }
    return render(request, 'libros/usuarios_mas_activos.html', context)

def eventos_organizados_por_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)  # Obtén el usuario o 404 si no existe
    cantidad_eventos = usuario.eventos_organizados.count()  # Cuenta los eventos organizados por el usuario

    context = {
        'usuario': usuario,
        'cantidad_eventos': cantidad_eventos,
    }
    return render(request, 'libros/eventos_organizados_por_usuario.html', context)