
import hashlib
from django.db import models
from django.utils.translation import ugettext_lazy as _

PACKAGES_CHOICES = (
    ('E1', _('Estudiante No IEEE')),
    ('E2', _('Estudiante IEEE')),
    ('E3', _('Estudiante IEEE & EMB')),
    ('P1', _('Profesional No IEEE')),
    ('P2', _('Profesional IEEE')),
    ('P3', _('Profesional IEEE & EMB')),
)


class Attend(models.Model):
    name = models.CharField(
        max_length=100,
        help_text='Nombres de la persona registrada.',
        verbose_name='Nombres.',
    )

    surname = models.CharField(
        max_length=100,
        help_text='Apellidos de la persona registrada.',
        verbose_name='Apellidos.',
    )

    email = models.EmailField(
        help_text='Nombres de la persona registrada.',
        verbose_name='Correo Electronico.',
    )

    address = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text='Direccion de la persona registrada.',
        verbose_name='Direccion.',
    )

    depot = models.CharField(
        max_length=100,
        help_text='Nro. del Deposito Bancario de la persona registrada.',
        verbose_name='Deposito.',
    )

    city = models.CharField(
        max_length=100,
        help_text='Ciudad de la persona registrada.',
        verbose_name='Ciudad.',
    )

    package = models.CharField(
        max_length=10,
        help_text='Paquete seleccionado.',
        verbose_name='Paquete.',
        choices=PACKAGES_CHOICES,
        default="E1",
    )

    class Meta:
        verbose_name = "Persona Registrada"
        verbose_name_plural = "Personas Registradas"

    def __str__(self):
        return "%s %s" % (self.name, self.surname)


class Suscriptor(models.Model):
    email = models.EmailField(
        blank=True,
        null=True,
        help_text='Correo Electronico del suscriptor.',
        verbose_name='Correo Electronico.',
    )

    date = models.DateTimeField(
        auto_now=True,
        help_text='Fecha del registro.',
        verbose_name='Fecha.',
    )

    class Meta:
        verbose_name = "Suscriptor"
        verbose_name_plural = "Suscriptores"

    def __str__(self):
        return "%s %s" % (self.email, self.date)


class Contact(models.Model):
    name = models.CharField(
        help_text='Correo Electronico del suscriptor.',
        verbose_name='Correo Electronico.',
        max_length=100,
    )

    email = models.EmailField(
        help_text='Correo Electronico del suscriptor.',
        verbose_name='Correo Electronico.',
    )

    message = models.TextField(
        help_text='Mensaje enviado.',
        verbose_name='Mensaje.',
    )

    class Meta:
        verbose_name = "Contacto"
        verbose_name_plural = "Mensajes de contacto"

    def __str__(self):
        return "%s %s" % (self.email, self.message)


def file_to(instance, filename):
    return '/'.join(['expositores', filename])

class Speaker(models.Model):
    full_name = models.CharField(
        help_text='e.g. Victor Aguilar',
        verbose_name='Nombre Completo.',
        max_length=200,
    )

    organization = models.CharField(
        help_text='e.g. Universidad Mayor de San Andres',
        verbose_name='Organizacion.',
        max_length=200,
    )

    bio = models.TextField(
        help_text='Descripcion corta',
        verbose_name='Bio.',
    )

    banner = models.ImageField(
        help_text='Sube una imagen',
        verbose_name='Infografia.',
        upload_to='infographies/%Y/%m/%d',
    )

    photo = models.ImageField(
        help_text='Sube una imagen',
        verbose_name='Fotografia.',
        upload_to='photos/%Y/%m/%d',
    )

    info = models.FileField(
        help_text='Sube un archivo PDF',
        verbose_name='Hoja de vida.',
        upload_to='cvs/%Y/%m/%d',
    )


    class Meta:
        verbose_name = "Expositor"
        verbose_name_plural = "Expositores"

    def __str__(self):
        return "%s %s" % (self.full_name, self.organization)


class Staff(models.Model):
    full_name = models.CharField(
        help_text='e.g. Victor Aguilar',
        verbose_name='Nombre Completo.',
        max_length=200,
    )

    role = models.CharField(
        help_text='Describe un Rol',
        verbose_name='Rol.',
        max_length=20,
    )

    photo = models.ImageField(
        help_text='Sube una imagen',
        verbose_name='Foto',
        upload_to='photos/%Y/%m/%d',
    )

    website = models.URLField(
        help_text='e.g. http://jvacx.com',
        verbose_name='Pagina',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Organizador"
        verbose_name_plural = "Organizadores"

    def __str__(self):
        return "%s %s" % (self.full_name, self.role)

class Sponsor(models.Model):
    name = models.CharField(
        help_text='e.g. Coca Cola',
        verbose_name='Empresa.',
        max_length=100,
    )

    website = models.URLField(
        help_text='e.g. http://jvacx.com',
        verbose_name='Pagina',
        blank=True,
        null=True,
    )

    logo = models.ImageField(
        help_text='Sube una imagen',
        verbose_name='Logo',
        upload_to='logo/%Y/%m/%d',
    )

    class Meta:
        verbose_name = "Auspiciador"
        verbose_name_plural = "Auspiciadores"

    def __str__(self):
        return "%s %s" % (self.name, self.logo)