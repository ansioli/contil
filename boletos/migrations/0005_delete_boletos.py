# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boletos', '0004_auto_20180121_1518'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Boletos',
        ),
    ]
