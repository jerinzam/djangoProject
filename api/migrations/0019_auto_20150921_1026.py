# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_auto_20150921_1006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_doc',
            field=models.ForeignKey(related_name='order_doc', to='api.Document'),
        ),
        migrations.AlterField(
            model_name='order',
            name='shop',
            field=models.ForeignKey(related_name='order_shop', to='api.Shop'),
        ),
    ]
