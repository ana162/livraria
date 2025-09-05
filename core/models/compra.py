from django.db import models
from rest_framework.serializers import CharField, ModelSerializer

from .livro import Livro
from .user import User


class CompraSerializer(ModelSerializer):
    usuario = CharField(source='usuario.email', read_only=True)  # inclua essa linha


class ItensCompra(models.Model):
    compra = models.ForeignKey('Compra', on_delete=models.CASCADE, related_name='itens')
    livro = models.ForeignKey(Livro, on_delete=models.PROTECT, related_name='+')
    quantidade = models.IntegerField(default=1)
    preco = models.DecimalField(max_digits=7, decimal_places=2, default=0)  # noqa: E305

class CompraSerializer(ModelSerializer):  # noqa: E302, F811
    status = CharField(source='get_status_display', read_only=True)  # inclua essa linha


class Compra(models.Model):
    class StatusCompra(models.IntegerChoices):
        CARRINHO = 1, "Carrinho"
        FINALIZADO = 2, "Realizado"
        PAGO = 3, "Pago"
        ENTREGUE = 4, "Entregue"
        tipo_pagamento = models.IntegerField(choices=TipoPagamento.choices, default=tipo_pagamento.CARTAO_CREDITO)  # type: ignore # noqa: F821


    class TipoPagamento(models.IntegerChoices):  # noqa: E302, E303
        CARTAO_CREDITO = 1, 'Cartão de Crédito'  # noqa: E117
        CARTAO_DEBITO = 2, 'Cartão de Débito'
        PIX = 3, 'PIX'
        BOLETO = 4, 'Boleto'
        TRANSFERENCIA_BANCARIA = 5, 'Transferência Bancária'
        DINHEIRO = 6, 'Dinheiro'
        OUTRO = 7, 'Outro'

    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name="compras")  # noqa: E305
    status = models.IntegerField(choices=StatusCompra.choices, default=StatusCompra.CARRINHO)  # noqa: F821
    data = models.DateTimeField(auto_now_add=True)  # campo novo  # noqa: W292
  # noqa: E114, W391
