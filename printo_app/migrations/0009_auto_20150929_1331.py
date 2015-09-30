# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('printo_app', '0008_auto_20150929_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='display_doc',
            field=models.FileField(blank=True, upload_to='documents'),
        ),
    ]
