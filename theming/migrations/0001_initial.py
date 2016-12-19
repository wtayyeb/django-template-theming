# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

from theming.models import thememanager


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteTheme',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('theme_slug', models.CharField(max_length=100, choices=thememanager.get_themes_choice())),
                ('site', models.OneToOneField(to='sites.Site')),
            ],
        ),
    ]
