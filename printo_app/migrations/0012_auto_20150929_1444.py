# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('printo_app', '0011_auto_20150929_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='tags',
            field=models.ManyToManyField(default='parvathy', blank=True, null=True, to='printo_app.Tag'),
        ),
    ]
