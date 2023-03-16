from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group, Permission
from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver

class UsuarioManager(BaseUserManager):
    def _create_user(self, dni, password, is_staff, is_superuser, **extra_fields):
        if not dni:
            raise ValueError('El DNI es obligatorio.')
        
        # Validar campos obligatorios
        nombre = extra_fields.get('nombre')
        apellido = extra_fields.get('apellido')
        email = extra_fields.get('email')
        telefono = extra_fields.get('telefono')
        if not nombre:
            raise ValueError('El nombre es obligatorio.')
        if not apellido:
            raise ValueError('El apellido es obligatorio.')
        if not email:
            raise ValueError('El email es obligatorio.')
        

        user = self.model(
            dni=dni,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, dni, password=None, **extra_fields):
        return self._create_user(dni, password, False, False, **extra_fields)


    def create_superuser(self, dni, password=None, **extra_fields):
        return self._create_user(dni, password, True, True, **extra_fields)


class Usuario(AbstractBaseUser):
    dni = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    email = models.EmailField(max_length=60)
    telefono = models.CharField(max_length=12)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    grupos = models.ManyToManyField(
        Group,
        verbose_name='grupos',
        blank=True,
        help_text='Los grupos a los que pertenece el usuario.',
        related_name='usuarios_grupos')
    permisos = models.ManyToManyField(
        Permission,
        verbose_name='permisos',
        blank=True,
        help_text='Permisos específicos para este usuario.',
        related_name='usuarios_permisos')

    USERNAME_FIELD = 'dni'
    REQUIRED_FIELDS = ['nombre', 'apellido', 'email', 'telefono']

    objects = UsuarioManager()
    def get_full_name(self):
        return f'{self.nombre} {self.apellido}'
    @property
    def get_short_name(self):
        return self.nombre
    @property
    def __str__(self):
        return f'{self.nombre} {self.apellido}'

class Paciente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    direccion = models.CharField(max_length=70)
    instagram = models.CharField(max_length=50, null=True, blank=True)
    facebook = models.CharField(max_length=50, null=True, blank=True)
    numero_obra_social = models.CharField(max_length=50, null=True, blank=True)
    obras_sociales = models.ManyToManyField('ObraSocial', blank=True)
    

    class Meta:
        verbose_name='Paciente'
        verbose_name_plural = 'Pacientes'
    def __str__(self):
        return f'{self.usuario.nombre} {self.usuario.apellido}'

class Medico(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    especialidades = models.ManyToManyField('EspecialidadMedica')
    matricula = models.IntegerField()
    obra_social = models.ManyToManyField('ObraSocial', blank=True, through='PrecioConsulta')

    class Meta:
        verbose_name='Medico'
        verbose_name_plural = 'Medicos'

    def __str__(self):
        return f'{self.usuario.nombre} {self.usuario.apellido}'

class EspecialidadMedica(models.Model):
    nombre = models.CharField(max_length=100)
    medicos = models.ManyToManyField('Medico')

    class Meta:
        verbose_name_plural = 'Especialidades'
    
    def __str__(self):
        return self.nombre

class ObraSocial(models.Model):
    nombre = models.CharField(max_length=100)
    medicos = models.ManyToManyField('Medico', blank=True, through='PrecioConsulta')
    pacientes = models.ManyToManyField('Paciente', blank=True)
    
    def __str__(self):
        return self.nombre

class PrecioConsulta(models.Model):
    medico = models.ForeignKey('Medico', on_delete=models.CASCADE)
    obra_social = models.ForeignKey('ObraSocial', on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_vigencia = models.DateField()

    def __str__(self):
        return f'{self.medico} - {self.obra_social}: {self.precio}'

class Turno(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    obra_social = models.ForeignKey(ObraSocial, on_delete=models.SET_NULL, null=True, blank=True)
    confirmado = models.BooleanField(default=False)
    class Meta:
        ordering = ['fecha', 'hora']
    def __str__(self):
        return f'Turno con {self.paciente} el {self.fecha} a las {self.hora}'



    
@receiver(post_save, sender=Turno)    
def crear_consulta(sender, instance, created, **kwargs):
    if instance.confirmado:
        obra_social = instance.obra_social
        if obra_social:
            precio = instance.medico.obra_social.through.objects.get(
                medico=instance.medico,
                obra_social=obra_social
            ).precio
        else:
            precio = instance.medico.obra_social.through.objects.filter(
                medico=instance.medico
            ).first().precio
        Consulta.objects.create(turno=instance, precio=precio)

class Consulta(models.Model):
    turno = models.OneToOneField(Turno, on_delete=models.CASCADE, related_name='consulta')
    precio = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'Consulta de {self.turno.paciente} con {self.turno.medico} el {self.turno.fecha} a las {self.turno.hora}'