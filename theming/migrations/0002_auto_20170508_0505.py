# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theming', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitetheme',
            name='site_description',
            field=models.CharField(default=b'', max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='sitetheme',
            name='site_title',
            field=models.CharField(default=b'', max_length=255, blank=True),
        ),
    ]
