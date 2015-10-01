# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('printo_app', '0004_auto_20151001_2122'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='docCount',
            field=models.IntegerField(default=0),
        ),
    ]
