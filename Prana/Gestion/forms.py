from django import forms
import re
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, EmailValidator
from .models import Usuario, Paciente
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField
########################### FORMULARIOS DE USUARIO ############################################
class Crear_usuario_form(forms.ModelForm):
    """
    Formulario para crear un nuevo usuario.
    """
    class Meta:
        model = Usuario
        fields = ['dni', 'nombre', 'apellido', 'email', 'telefono', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    dni = forms.IntegerField(
        validators=[MinValueValidator(1000000), MaxValueValidator(99999999)],
        error_messages={
            'min_value': 'El DNI debe tener al menos 7 dígitos.',
            'max_value': 'El DNI no puede tener más de 8 dígitos.',
            'unique': 'El DNI ingresado ya existe. Por favor, ingrese otro DNI.',
        }
    )
    nombre = forms.CharField(max_length=30, 
        validators=[MinLengthValidator(2)],
        error_messages={
            'min_value': 'El nombre debe contener al menos 2 caracteres.'})
    apellido = forms.CharField(max_length=30,
         validators=[MinLengthValidator(2)],
         error_messages={
            'min_value': 'El Apellido debe tener al menos 7 dígitos.'})
    email = forms.EmailField(max_length=60, 
        validators=[EmailValidator()],
        error_messages={
            'min_value': 'Ingrese un Email valido.'})
    telefono = forms.CharField(max_length=12)
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Confirmar contraseña')
    def clean(self):
        cleaned_data = super().clean()

        # Aquí puedes agregar validaciones personalizadas que involucren múltiples campos.
        # Por ejemplo, verificar que el email no esté siendo usado por otro usuario:
        

        # Verificar que la contraseña tenga al menos 8 caracteres, una mayúscula y un número
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        
        
        if not  any(char.isupper() for char in password) or len(password) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres y una mayúscula .")
        if password != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
    def save(self, commit=True):
        # Guardar la contraseña cifrada en lugar de la contraseña en texto plano
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        
        if commit:
            user.save()
            
        return user
    
class Modificar_usuario_form(forms.ModelForm):
    """
    Formulario para actualizar los detalles de un usuario.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Usuario
        fields = ( 'dni','nombre', 'apellido', 'email', 'telefono')


######################### FORMULARIO DE PACIENTES #########################################

class Crear_paciente_form(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['direccion', 'instagram', 'facebook', 'numero_obra_social', 'obras_sociales']

    usuario = forms.ModelChoiceField(queryset=Usuario.objects.all(), widget=forms.HiddenInput(), required=False)



