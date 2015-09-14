# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20150913_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='company_name',
            field=models.CharField(null=True, max_length=100),
        ),
    ]
