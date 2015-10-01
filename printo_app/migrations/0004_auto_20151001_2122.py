# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('printo_app', '0003_auto_20151001_2120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='rate',
            field=models.IntegerField(default=0.0),
        ),
    ]
