# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('printo_app', '0005_auto_20150929_0747'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='userType',
            field=models.CharField(default=None, max_length=20, choices=[('1', 'owner'), ('2', 'student'), ('3', 'Private person')]),
        ),
    ]
