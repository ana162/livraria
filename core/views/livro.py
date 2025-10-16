from core.serializers.livro import LivroMaisVendidoSerializer  # noqa: I001
from django.db.models.query_utils import Q
from django_filters.rest_framework import DjangoFilterBackend  # noqa: I001
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter  # noqa: F401
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter  # noqa: F811

from core.models import Compra, Livro
from core.serializers import (
    LivroAlterarPrecoSerializer,
    LivroListSerializer,
    LivroRetrieveSerializer,
    LivroSerializer,
)


class LivroViewSet(ModelViewSet):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['categoria__descricao', 'editora__nome']  # Acrescentando o filtro por editora
    search_fields = ['titulo']
    ordering_fields = ['titulo', 'preco']
    ordering = ['titulo']

    def get_serializer_class(self):
        if self.action == "list":
            return LivroListSerializer
        elif self.action == "retrieve":
            return LivroRetrieveSerializer
        return LivroSerializer

    @extend_schema(
        request=LivroAlterarPrecoSerializer,
        responses={200: None},
        description="Altera o preço do livro especificado.",
        summary="Alterar preço do livro",
    )
    @action(detail=True, methods=['patch'])
    def alterar_preco(self, request, pk=None):
        livro = self.get_object()

        serializer = LivroAlterarPrecoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        livro.preco = serializer.validated_data['preco']
        livro.save()

        return Response(
            {'detail': f'Preço do livro "{livro.titulo}" atualizado para {livro.preco}.'}, status=status.HTTP_200_OK
        )

    @extend_schema(
        summary="Lista os livros mais vendidos",
        description="Retorna os livros que venderam mais de 10 unidades.",
        responses={
            200: LivroMaisVendidoSerializer(many=True)  # noqa: F821
        },
    )
    @action(detail=False, methods=['get'])
    def mais_vendidos(self, request):
        livros = Livro.objects.annotate(
            total_vendidos=sum(  # noqa: F821
                'itens_compra__quantidade',
                filter=Q(itens_compra__compra__status=Compra.StatusCompra.FINALIZADO)  # noqa: F821
            )
        ).filter(total_vendidos__gt=100).order_by('-total_vendidos')

        serializer = LivroMaisVendidoSerializer(livros, many=True)

        if not serializer.data:
            return Response(
                {"detail": "Nenhum livro excedeu 10 vendas."},
                status=status.HTTP_200_OK
            )
