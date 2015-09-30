# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('printo_app', '0006_userprofile_usertype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='userType',
            field=models.IntegerField(choices=[(1, 'owner'), (2, 'employee'), (3, 'Private person')]),
        ),
    ]
