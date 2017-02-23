# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('day', models.DateField(serialize=False, primary_key=True)),
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
                ('xl', models.BooleanField()),
                ('observation', models.TextField()),
                ('selected_item', models.ForeignKey(to='noras_menu.MenuItems')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='userselectedlunch',
            unique_together=set([('user', 'selected_item')]),
        ),
        migrations.AlterUniqueTogether(
            name='menuitems',
            unique_together=set([('name', 'menu')]),
        ),
    ]
