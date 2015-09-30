# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('printo_app', '0004_auto_20150928_1114'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('profile_picture', models.ImageField(null=True, upload_to='documents', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='document',
            name='pageNoRange',
            field=models.CharField(max_length=100, default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='document',
            name='publisher',
            field=models.ForeignKey(to='printo_app.Publisher', null=True, blank=True),
        ),
    ]
