# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boletos', '0006_boleto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boleto',
            name='vencimento',
            field=models.DateField(),
            preserve_default=True,
        ),
    ]
