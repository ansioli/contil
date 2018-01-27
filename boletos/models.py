from django.db import models

# Create your models here.
class Boletos(models.Model):
    id = models.CharField(max_length=10,null=False,primary_key=True,unique=True)
    vencimento = models.CharField(max_length=12,null=False)
    valor = models.CharField(max_length=10,null=False)
    status = models.CharField(max_length=6,null=False)