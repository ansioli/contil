# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boletos', '0007_auto_20180121_2141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boleto',
            name='vencimento',
            field=models.CharField(max_length=12),
            preserve_default=True,
        ),
    ]
