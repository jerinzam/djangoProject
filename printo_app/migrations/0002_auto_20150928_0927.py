# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('printo_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('shopName', models.CharField(max_length=100)),
                ('employee', models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='shop_employee')),
                ('owner', models.ForeignKey(related_name='shop_owner', to='printo_app.Organization')),
            ],
        ),
        migrations.AddField(
            model_name='document',
            name='shop',
            field=models.ForeignKey(default=2, to='printo_app.Shop'),
            preserve_default=False,
        ),
    ]
