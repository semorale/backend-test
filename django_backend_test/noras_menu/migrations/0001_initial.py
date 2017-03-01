# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('menu_uuid', models.UUIDField(default=uuid.uuid4, unique=True, editable=False)),
                ('day', models.DateField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MenuItems',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('menu', models.ForeignKey(to='noras_menu.Menu')),
            ],
        ),
        migrations.CreateModel(
            name='Subscribers',
            fields=[
                ('email', models.EmailField(max_length=254, serialize=False, primary_key=True)),
                ('full_name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='UserSelectedLunch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=128)),
                ('xl', models.BooleanField(default=False)),
                ('observation', models.TextField()),
                ('menu', models.ForeignKey(to='noras_menu.Menu')),
                ('selected_item', models.ForeignKey(to='noras_menu.MenuItems')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='userselectedlunch',
            unique_together=set([('user', 'menu')]),
        ),
        migrations.AlterUniqueTogether(
            name='menuitems',
            unique_together=set([('name', 'menu')]),
        ),
    ]
