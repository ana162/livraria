from django.db import models

from .livro import Livro  # noqa: F401
from .user import User


class Compra(models.Model):
    class StatusCompra(models.IntegerChoices):
        CARRINHO = 1, "Carrinho"
        FINALIZADO = 2, "Realizado"
        PAGO = 3, "Pago"
        ENTREGUE = 4, "Entregue"

    class TipoPagamento(models.IntegerChoices):  # noqa: E302, E303
        CARTAO_CREDITO = 1, 'Cartão de Crédito'  # noqa: E117
        CARTAO_DEBITO = 2, 'Cartão de Débito'
        PIX = 3, 'PIX'
        BOLETO = 4, 'Boleto'
        TRANSFERENCIA_BANCARIA = 5, 'Transferência Bancária'
        DINHEIRO = 6, 'Dinheiro'
        OUTRO = 7, 'Outro'

    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name='compras')
    status = models.IntegerField(choices=StatusCompra.choices, default=StatusCompra.CARRINHO)
    tipo_pagamento = models.IntegerField(choices=TipoPagamento.choices, default=TipoPagamento.CARTAO_CREDITO)
    data = models.DateTimeField(auto_now_add=True)  # campo novo

    @property
    def total(self):
        return sum(item.preco * item.quantidade for item in self.itens.all())

    def __str__(self):
        return f'({self.id}) {self.usuario} {self.status}'


class ItensCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='itens')  # type: ignore  # noqa: E112, F821
    livro = models.ForeignKey(Livro, on_delete=models.PROTECT, related_name='itenscompra')
    quantidade = models.IntegerField(default=1)
    preco = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)  # noqa: W292


    def __str__(self):  # noqa: E303, F811
        return f'({self.id}) {self.compra} {self.livro} {self.quantidade}'  # noqa: W292
