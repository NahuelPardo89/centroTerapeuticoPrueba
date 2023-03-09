from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, logout,login
from django.contrib import messages

def is_medico(user):
    return user.groups.filter(name='medicos').exists()

def is_paciente(user):
    return user.groups.filter(name='pacientes').exists()

def is_secretaria(user):
    return user.groups.filter(name='secretarias').exists()

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
        username = request.POST['dni']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
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

