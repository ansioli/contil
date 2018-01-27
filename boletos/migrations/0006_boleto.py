# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boletos', '0005_delete_boletos'),
    ]

    operations = [
        migrations.CreateModel(
            name='Boleto',
            fields=[
                ('id', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('vencimento', models.CharField(max_length=12)),
                ('valor', models.CharField(max_length=10)),
                ('status', models.CharField(max_length=6)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
