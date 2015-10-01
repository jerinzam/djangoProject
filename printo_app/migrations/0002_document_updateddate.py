# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('printo_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='updatedDate',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]
