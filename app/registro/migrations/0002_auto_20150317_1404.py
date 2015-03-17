# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='name',
            field=models.CharField(help_text=b'Correo Electronico del suscriptor.', max_length=100, verbose_name=b'Correo Electronico.'),
            preserve_default=True,
        ),
    ]
