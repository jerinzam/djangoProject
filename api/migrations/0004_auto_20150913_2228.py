# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20150913_2217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='company_name',
            field=models.CharField(max_length=100, blank=True, null=True),
        ),
    ]
