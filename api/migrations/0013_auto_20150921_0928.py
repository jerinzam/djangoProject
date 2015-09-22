# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0012_shop_employee'),
    ]

    operations = [
        migrations.RenameField(
            model_name='document',
            old_name='id',
            new_name='doc_id',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='org_user',
        ),
        migrations.RemoveField(
            model_name='shop',
            name='shopowner',
        ),
        migrations.AddField(
            model_name='organization',
            name='employee',
            field=models.ManyToManyField(related_name='org_employee', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='organization',
            name='owner',
            field=models.ForeignKey(related_name='org_owner', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shop',
            name='owner',
            field=models.ForeignKey(related_name='shop_owner', default=2, to='api.Organization'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='document',
            name='owner',
            field=models.ForeignKey(related_name='doc_owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='order',
            name='shop',
            field=models.ForeignKey(to='api.Shop'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='employee',
            field=models.ForeignKey(related_name='shop_emp', to=settings.AUTH_USER_MODEL),
        ),
    ]
