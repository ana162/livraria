from rest_framework.viewsets import ModelViewSet  # noqa: I001
from rest_framework import status  # noqa: F401
from rest_framework.decorators import action
from rest_framework.response import Response  # noqa: F401
from rest_framework.viewsets import ModelViewSet  # noqa: F811
from core.models import Livro
from core.serializers import (
    LivroAlterarPrecoSerializer,
    LivroListSerializer,
    LivroRetrieveSerializer,
    LivroSerializer,
)


class LivroViewSet(ModelViewSet):  # noqa: E303
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer

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

    def get_serializer_class(self):
        if self.action == "list":
            return LivroListSerializer  # type: ignore # noqa: F821
        elif self.action == "retrieve":
            return LivroRetrieveSerializer # type: ignore  # noqa: E261, F821
        return LivroSerializer
