# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boletos', '0002_auto_20180121_1452'),
    ]

    operations = [
        migrations.CreateModel(
            name='Boleto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cobrancaID', models.CharField(max_length=10)),
                ('vencimento', models.CharField(max_length=12)),
                ('valor', models.CharField(max_length=10)),
                ('pagamento', models.CharField(max_length=7)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
