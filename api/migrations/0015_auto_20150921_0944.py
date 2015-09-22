# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20150921_0929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='employee',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, null=True, related_name='org_employee'),
        ),
    ]
