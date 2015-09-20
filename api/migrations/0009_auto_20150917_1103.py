# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='doc_name',
            new_name='order_doc',
        ),
    ]
