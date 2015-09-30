# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('printo_app', '0010_auto_20150929_1436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='tags',
            field=models.ManyToManyField(null=True, blank=True, to='printo_app.Tag'),
        ),
    ]
