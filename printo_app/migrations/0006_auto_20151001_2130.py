# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('printo_app', '0005_organization_doccount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='rate',
            field=models.DecimalField(default=0.0, max_digits=4, decimal_places=2),
        ),
    ]
