# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attend',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Nombres de la persona registrada.', max_length=100, verbose_name=b'Nombres.')),
                ('surname', models.CharField(help_text=b'Apellidos de la persona registrada.', max_length=100, verbose_name=b'Apellidos.')),
                ('email', models.EmailField(help_text=b'Nombres de la persona registrada.', max_length=75, verbose_name=b'Correo Electronico.')),
                ('address', models.CharField(help_text=b'Direccion de la persona registrada.', max_length=200, null=True, verbose_name=b'Direccion.', blank=True)),
                ('depot', models.CharField(help_text=b'Nro. del Deposito Bancario de la persona registrada.', max_length=100, verbose_name=b'Deposito.')),
                ('city', models.CharField(help_text=b'Ciudad de la persona registrada.', max_length=100, verbose_name=b'Ciudad.')),
                ('package', models.CharField(default=b'E1', help_text=b'Paquete seleccionado.', max_length=10, verbose_name=b'Paquete.', choices=[(b'E1', 'Estudiante No IEEE'), (b'E2', 'Estudiante IEEE'), (b'E3', 'Estudiante IEEE & EMB'), (b'P1', 'Profesional No IEEE'), (b'P2', 'Profesional IEEE'), (b'P3', 'Profesional IEEE & EMB')])),
            ],
            options={
                'verbose_name': 'Persona Registrada',
                'verbose_name_plural': 'Personas Registradas',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.EmailField(help_text=b'Correo Electronico del suscriptor.', max_length=75, verbose_name=b'Correo Electronico.')),
                ('email', models.EmailField(help_text=b'Correo Electronico del suscriptor.', max_length=75, verbose_name=b'Correo Electronico.')),
                ('message', models.TextField(help_text=b'Mensaje enviado.', verbose_name=b'Mensaje.')),
            ],
            options={
                'verbose_name': 'Contacto',
                'verbose_name_plural': 'Mensajes de contacto',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Suscriptor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(help_text=b'Correo Electronico del suscriptor.', max_length=75, null=True, verbose_name=b'Correo Electronico.', blank=True)),
                ('date', models.DateTimeField(help_text=b'Fecha del registro.', verbose_name=b'Fecha.', auto_now=True)),
            ],
            options={
                'verbose_name': 'Suscriptor',
                'verbose_name_plural': 'Suscriptores',
            },
            bases=(models.Model,),
        ),
    ]
