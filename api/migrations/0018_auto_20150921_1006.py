# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_auto_20150921_0956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='owner',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='org_owner'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='employee',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='shop_emp'),
        ),
    ]
