from django.shortcuts import render, redirect

# Create your views here.

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, logout,login,get_user_model
from django.contrib import messages
from .forms import  Crear_usuario_form
from .models import Usuario
def is_medico(user):
    return user.grupos.filter(name='medicos').exists()

def is_paciente(user):
    return user.grupos.filter(name='pacientes').exists()

def is_secretaria(user):
    return user.grupos.filter(name='secretarias').exists()

def home(request):
    if not request.user.is_authenticated:
        return render(request,'home_unauthenticated.html')
    elif is_medico(request.user):
        return redirect('home_medico')
    elif is_paciente(request.user):
        return redirect('home_paciente')
    elif is_secretaria(request.user):
        return redirect('home_secretaria')
    else:
        return redirect('home_medico')

@login_required
#@user_passes_test(is_medico)
def home_medico(request):
    # Código para la plantilla home_medico.html
    return render(request, 'medicos/home_medico.html')

@login_required
@user_passes_test(is_paciente)
def home_paciente(request):
    # Código para la plantilla home_paciente.html
    return render(request, 'pacientes/home_paciente.html')

@login_required
@user_passes_test(is_secretaria)
def home_secretaria(request):
    # Código para la plantilla home_secretaria.html
    return render(request, 'secretaria/home_secretaria.html')

@login_required
def home_unauthenticated(request):
    # Código para la plantilla home_unauthenticated.html
    return render(request, 'home_unauthenticated.html')
def login_view(request):
    if request.method == 'POST':
        dni = request.POST['dni']
        password = request.POST['password']
        
        user = authenticate(request, dni=dni, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "El DNI o la contraseña no son válidos.")
            return redirect('login')
    else:
        return render(request, 'login.html')

@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('home')






def crear_usuario(request):
    if request.method == 'POST':
        form = Crear_usuario_form(request.POST)
        if form.is_valid():
            usuario = form.save()
            messages.success(request, 'Usuario creado con éxito.')
            return redirect('home')
        else:
            messages.error(request, 'Por favor corrija los errores a continuación.')
            return render(request, 'crear_usuario.html', {'form': form})
    else:
        form = Crear_usuario_form()
    return render(request, 'crear_usuario.html', {'form': form})

"""
def crear_paciente(request):
    if request.method == 'POST':
        usuario_form = Crear_usuario_form(request.POST)
        paciente_form = Crear_Paciente_form(request.POST)
        if usuario_form.is_valid() and paciente_form.is_valid():
            usuario = usuario_form.save()
            usuario.groups.add('Pacientes') # Agrega el usuario al grupo 'Pacientes'
            paciente = paciente_form.save(commit=False)
            paciente.usuario_ptr = usuario
            paciente.save()
            return redirect('perfil_paciente', paciente.pk)
    else:
        usuario_form = Crear_usuario_form()
        paciente_form = Crear_Paciente_form()
    return render(request, 'crear_paciente.html', {'usuario_form': usuario_form, 'paciente_form': paciente_form})

"""

