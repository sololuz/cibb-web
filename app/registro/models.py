
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