# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DocType',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('docType', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('uuid', models.CharField(max_length=60, blank=True, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('display_doc', models.FileField(upload_to='display_docs/', blank=True)),
                ('display', models.BooleanField(default=True)),
                ('is_public', models.BooleanField(default=False)),
                ('is_user_private', models.BooleanField(default=False)),
                ('pages', models.IntegerField()),
                ('price', models.DecimalField(max_digits=6, decimal_places=2)),
                ('uploadedDate', models.DateTimeField(auto_now_add=True)),
                ('updatedDate', models.DateTimeField(auto_now=True)),
                ('edition', models.IntegerField()),
                ('author_names', models.TextField()),
                ('course', models.ManyToManyField(blank=True, to='printo_app.Course')),
                ('doc_type', models.ForeignKey(to='printo_app.DocType')),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('employee', models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL, blank=True, related_name='org_employee')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='org_owner')),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('code', models.CharField(max_length=4)),
            ],
        ),
        migrations.AddField(
            model_name='document',
            name='organization',
            field=models.ForeignKey(null=True, to='printo_app.Organization', blank=True, related_name='doc_owner'),
        ),
        migrations.AddField(
            model_name='document',
            name='private_user',
            field=models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='document',
            name='publisher',
            field=models.ForeignKey(null=True, to='printo_app.Publisher'),
        ),
        migrations.AddField(
            model_name='document',
            name='tags',
            field=models.ManyToManyField(to='printo_app.Tag'),
        ),
        migrations.AddField(
            model_name='document',
            name='topic',
            field=models.ManyToManyField(blank=True, to='printo_app.Topic'),
        ),
        migrations.AddField(
            model_name='document',
            name='university',
            field=models.ManyToManyField(blank=True, to='printo_app.University'),
        ),
        migrations.AddField(
            model_name='college',
            name='university',
            field=models.ForeignKey(null=True, to='printo_app.University'),
        ),
    ]
