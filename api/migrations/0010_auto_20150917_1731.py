# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20150917_1103'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='comments',
            field=models.CharField(max_length=100, default=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='shop',
            field=models.ForeignKey(to='api.UserProfile', default=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(max_length=20, default='ground'),
            preserve_default=False,
        ),
    ]
