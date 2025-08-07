from django.db import models

from .livro import Livro
from .user import User
from rest_framework.serializers import CharField, ModelSerializer
class CompraSerializer(ModelSerializer):
    usuario = CharField(source='usuario.email', read_only=True) # inclua essa linha

class ItensCompra(models.Model):
    compra = models.ForeignKey('Compra', on_delete=models.CASCADE, related_name='itens')
    livro = models.ForeignKey(Livro, on_delete=models.PROTECT, related_name='+')
    quantidade = models.IntegerField(default=1)


class Compra(models.Model):
    class StatusCompra(models.IntegerChoices):
        CARRINHO = 1, "Carrinho"
        FINALIZADO = 2, "Realizado"
        PAGO = 3, "Pago"
        ENTREGUE = 4, "Entregue"

    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name="compras")
    status = models.IntegerField(choices=StatusCompra.choices, default=StatusCompra.CARRINHO)
