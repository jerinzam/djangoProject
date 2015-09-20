# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_document'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('customer', models.CharField(max_length=100)),
                ('doc_name', models.ForeignKey(to='api.Document', related_name='orders')),
            ],
        ),
    ]
