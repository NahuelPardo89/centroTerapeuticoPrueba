from django import forms
import re
from .models import Usuario
from django.contrib.auth.models import Group


class Crear_usuario_form(forms.ModelForm):
    """
    Formulario para crear un nuevo usuario.
    """
    password1 = forms.CharField(
        label='Contraseña',
        strip=False,
        widget=forms.PasswordInput,
        help_text='La contraseña debe tener al menos 8 caracteres.'
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput,
        strip=False,
        
        help_text='Ingrese la misma contraseña que antes, para verificar.'
    )

    class Meta:
        model = Usuario
        fields = ('dni', 'nombre', 'apellido', 'email', 'telefono')

    def clean_password1(self):
        # Verificar si la contraseña tiene al menos 8 caracteres y al menos una letra mayúscula
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise forms.ValidationError('La contraseña debe tener al menos 8 caracteres.')
        if not re.search('[A-Z]', password1):
            raise forms.ValidationError('La contraseña debe contener al menos una letra mayúscula.')
        return password1

    def clean_password2(self):
        # Verificar si las dos contraseñas coinciden
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return password2

    def save(self, commit=True):
        # Guardar la contraseña cifrada en lugar de la contraseña en texto plano
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        
        if commit:
            user.save()
            grupo = Group.objects.get(name='secretarias')
            user.grupos.add(grupo)
        return user


"""
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario, Paciente, ObraSocial

from django.contrib.auth.forms import UserCreationForm
from django import forms

from django.contrib.auth.models import Group





class Crear_usuario_form(UserCreationForm):
    dni = forms.IntegerField( required=True, help_text='Requerido.')
    nombre = forms.CharField(max_length=30, required=True, help_text='Requerido.')
    apellido = forms.CharField(max_length=30, required=True, help_text='Requerido.')
    
    email = forms.EmailField(max_length=60, required=True, help_text='Requerido. Ingresa una dirección de correo válida.')
    telefono = forms.CharField(max_length=9, required=True, help_text='Requerido.')
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput, help_text="La contraseña debe tener al menos 8 caracteres y no puede ser demasiado común.")
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput, help_text='Ingresa la misma contraseña para confirmar.')

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if Usuario.objects.filter(dni=dni).exists():
            raise forms.ValidationError("Ya existe un usuario con este DNI.")
        return dni

    class Meta:
        model = Usuario
        fields = ('dni','nombre', 'apellido', 'email',  'telefono', 'password1', 'password2')
"""
"""
class Crear_paciente_form(forms.ModelForm):
    direccion = forms.CharField(max_length=70)
    instagram = forms.CharField(max_length=50, required=False)
    facebook = forms.CharField(max_length=50, required=False)
    numero_obra_social = forms.CharField(max_length=50, required=False)
    obras_sociales = forms.ModelMultipleChoiceField(queryset=ObraSocial.objects.all(), widget=forms.CheckboxSelectMultiple(), required=False)
    usuario_form = Crear_usuario_form()

    class Meta:
        model = Paciente
        fields = ('direccion', 'instagram', 'facebook', 'numero_obra_social', 'obras_sociales', 'usuario_form')

    def save(self, commit=True):
        usuario = self.cleaned_data['usuario_form'].save(commit=False)
        usuario.set_password(self.cleaned_data["usuario_form"].cleaned_data["password1"])
        usuario.save()
        grupo = Group.objects.get(name='Pacientes')
        usuario.groups.add(grupo)
        paciente = super().save(commit=False)
        paciente.usuario_ptr = usuario
        if commit:
            paciente.save()
            self.save_m2m()
        return paciente

class Crear_paciente_form(forms.ModelForm):
    direccion = forms.CharField(max_length=70)
    instagram = forms.CharField(max_length=50, required=False)
    facebook = forms.CharField(max_length=50, required=False)
    numero_obra_social = forms.CharField(max_length=50, required=False)
    obras_sociales = forms.ModelMultipleChoiceField(queryset=ObraSocial.objects.all(), widget=forms.CheckboxSelectMultiple(), required=False)

    # Clase interna para definir los campos de usuario
    class UsuarioForm(forms.ModelForm):
        class Meta:
            model = get_user_model()
            fields = ('nombre', 'apellido', 'email', 'dni', 'telefono', 'password1', 'password2')
        
        password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput, help_text="La contraseña debe tener al menos 8 caracteres y no puede ser demasiado común.")
        password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput, help_text='Ingresa la misma contraseña para confirmar.')

        def clean_dni(self):
            dni = self.cleaned_data.get('dni')
            if get_user_model().objects.filter(dni=dni).exists():
                raise forms.ValidationError("Ya existe un usuario con este DNI.")
            return dni

    usuario_form = UsuarioForm()

    class Meta:
        model = Paciente
        fields = ('direccion', 'instagram', 'facebook', 'numero_obra_social', 'obras_sociales', 'usuario_form')

    def save(self, commit=True):
        usuario = self.cleaned_data['usuario_form'].save(commit=False)
        usuario.set_password(self.cleaned_data["usuario_form"].cleaned_data["password1"])
        usuario.save()
        grupo = Group.objects.get(name='Pacientes')
        usuario.groups.add(grupo)
        paciente = super().save(commit=False)
        paciente.usuario_ptr = usuario
        if commit:
            paciente.save()
            self.save_m2m()
        return paciente

"""        