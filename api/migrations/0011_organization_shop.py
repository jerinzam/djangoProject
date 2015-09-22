# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userroles', '__first__'),
        ('api', '0010_auto_20150917_1731'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('org_id', models.AutoField(primary_key=True, serialize=False)),
                ('org_user', models.ForeignKey(to='userroles.UserRole')),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('shop_id', models.AutoField(primary_key=True, serialize=False)),
                ('shopName', models.CharField(max_length=100)),
                ('shopowner', models.ForeignKey(to='api.Organization', related_name='shops')),
            ],
        ),
    ]
