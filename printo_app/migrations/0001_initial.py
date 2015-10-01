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
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DocType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('docType', models.CharField(max_length=20)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('uuid', models.CharField(max_length=60, unique=True, blank=True)),
                ('name', models.CharField(max_length=200)),
                ('pageNoRange', models.CharField(max_length=100, null=True, blank=True)),
                ('display_doc', models.FileField(blank=True, upload_to='display_docs')),
                ('display', models.BooleanField(default=True)),
                ('is_public', models.BooleanField(default=False)),
                ('is_user_private', models.BooleanField(default=False)),
                ('pages', models.IntegerField()),
                ('price', models.DecimalField(max_digits=6, decimal_places=2)),
                ('edition', models.IntegerField(null=True, blank=True)),
                ('author_names', models.TextField(null=True, blank=True)),
                ('course', models.ManyToManyField(blank=True, to='printo_app.Course')),
                ('doc_type', models.ForeignKey(to='printo_app.DocType')),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('employee', models.ManyToManyField(null=True, blank=True, related_name='org_employee', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='org_owner')),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('shopName', models.CharField(max_length=100)),
                ('employee', models.ForeignKey(unique=True, related_name='shop_employee', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(to='printo_app.Organization', related_name='shop_owner')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('code', models.CharField(max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('profile_picture', models.ImageField(null=True, blank=True, upload_to='documents')),
                ('userType', models.IntegerField(choices=[(1, 'owner'), (2, 'employee'), (3, 'Private person')])),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='document',
            name='organization',
            field=models.ForeignKey(null=True, blank=True, related_name='doc_owner', to='printo_app.Organization'),
        ),
        migrations.AddField(
            model_name='document',
            name='private_user',
            field=models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='document',
            name='publisher',
            field=models.ForeignKey(null=True, blank=True, to='printo_app.Publisher'),
        ),
        migrations.AddField(
            model_name='document',
            name='tags',
            field=models.ManyToManyField(null=True, blank=True, to='printo_app.Tag'),
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
        migrations.AddField(
            model_name='branch',
            name='course',
            field=models.ForeignKey(to='printo_app.Course'),
        ),
    ]
