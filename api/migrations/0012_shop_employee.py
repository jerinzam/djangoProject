# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0011_organization_shop'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='employee',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL, related_name='shops'),
            preserve_default=False,
        ),
    ]
