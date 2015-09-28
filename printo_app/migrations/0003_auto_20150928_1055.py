# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('printo_app', '0002_auto_20150928_0927'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='shop',
        ),
        migrations.AlterField(
            model_name='document',
            name='author_names',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='edition',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='shop',
            name='employee',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True, related_name='shop_employee'),
        ),
    ]
