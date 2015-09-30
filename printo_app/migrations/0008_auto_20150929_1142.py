# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('printo_app', '0007_auto_20150929_0846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='pageNoRange',
            field=models.CharField(blank=True, null=True, max_length=100),
        ),
    ]
