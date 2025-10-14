from django.db import transaction
from django.utils import timezone
from drf_spectacular.utils import extend_schema  # noqa: F401
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.models import Compra
from core.serializers import CompraCreateUpdateSerializer, CompraListSerializer, CompraSerializer  # noqa: F401


class CompraViewSet(ModelViewSet):
    @action(detail=False, methods=['get'])
    def relatorio_vendas_mes(self, request):
        agora = timezone.now()
        inicio_mes = agora.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        compras = Compra.objects.filter(
            status=Compra.StatusCompra.FINALIZADO,
            data__gte=inicio_mes
        )

        total_vendas = sum(compra.total for compra in compras)
        quantidade_vendas = compras.count()

        return Response(
                {
                        "status": "Relatório de vendas deste mês",
                        "total_vendas": total_vendas,
                        "quantidade_vendas": quantidade_vendas,
                        "valor_medio_venda": total_vendas / quantidade_vendas if quantidade_vendas > 0 else 0,
                        "data_inicio": inicio_mes,
                },
                status=status.HTTP_200_OK,
        )
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer


    def get_queryset(self):  # noqa: E303
        usuario = self.request.user
        if usuario.is_superuser:
            return Compra.objects.all()
        if usuario.groups.filter(name='administradores'):
            return Compra.objects.all()
        return Compra.objects.filter(usuario=usuario)

    @action(detail=True, methods=["post"])
    def finalizar(self, request, pk=None):
        compra = self.get_object()

        # Checa se a compra já foi finalizada
        if compra.status != Compra.StatusCompra.CARRINHO:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'status': 'Compra já finalizada'}
            )

        # Garante integridade transacional durante a finalização
        with transaction.atomic():  # noqa: F821
            for item in compra.itens.all():

                # Valida se o estoque é suficiente para cada livro
                if item.quantidade > item.livro.quantidade:
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data={
                            'status': 'Quantidade insuficiente',
                            'livro': item.livro.titulo,
                            'quantidade_disponivel': item.livro.quantidade,
                        }
                    )

                # Atualiza o estoque dos livros
                item.livro.quantidade -= item.quantidade
                item.livro.save()

            # Finaliza a compra: atualiza status
            compra.status = Compra.StatusCompra.FINALIZADO
            compra.save()

        return Response(status=status.HTTP_200_OK, data={'status': 'Compra finalizada'})  # noqa: W292
