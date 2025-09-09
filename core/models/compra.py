from django.db import models

from .livro import Livro
from .user import User


class Compra(models.Model):  # noqa: E303
    compra = models.ForeignKey('self', on_delete=models.CASCADE, related_name='itens', null=True, blank=True)  # noqa: E111
    livro = models.ForeignKey(Livro, on_delete=models.PROTECT, related_name='+')
    quantidade = models.IntegerField(default=1)
    preco = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    class StatusCompra(models.IntegerChoices):
        CARRINHO = 1, 'Carrinho'
        FINALIZADO = 2, 'Realizado'
        PAGO = 3, 'Pago'
        ENTREGUE = 4, 'Entregue'

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
    tipo_pagamento = models.IntegerField(choices=TipoPagamento.choices, default=TipoPagamento.CARTAO_CREDITO)  # type: ignore # noqa: F821
    data = models.DateTimeField(auto_now_add=True)  # campo novo  # noqa: W292
# noqa: E114, W391
