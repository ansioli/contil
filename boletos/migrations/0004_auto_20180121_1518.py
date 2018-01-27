# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boletos', '0003_boleto'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Boleto',
            new_name='Boletos',
        ),
    ]
