"""Prana URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Gestion import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('home_medico/', views.home_medico, name='home_medico'),
    path('home_paciente/', views.home_paciente, name='home_paciente'),
    path('home_secretaria/', views.home_secretaria, name='home_secretaria'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('modificar_usuario_logged/', views.modificar_usuario_logged, name='modificar_usuario_logged'),
    path('modificar_usuario/<id>', views.modificar_usuario, name='modificar_usuario'),
    path('eliminar_usuario/<id>', views.eliminar_usuario, name='eliminar_usuario'),
    path('listar_usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('crear_paciente/', views.crear_paciente, name='crear_paciente'),
    path('listar_pacientes/', views.listar_pacientes, name='listar_pacientes'),
    path('modificar_paciente/<id>', views.modificar_paciente, name='modificar_paciente'),
    path('eliminar_paciente/<id>', views.eliminar_paciente, name='eliminar_paciente'),

    
]
