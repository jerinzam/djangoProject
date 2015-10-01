# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('printo_app', '0002_document_updateddate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='document',
            name='uploadedDate',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='shop',
            name='createdOn',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='shop',
            name='orderCount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='shop',
            name='rate',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='shop',
            name='services',
            field=models.ManyToManyField(to='printo_app.Service', blank=True),
        ),
    ]
