from rest_framework.serializers import (
    DecimalField,
    IntegerField,
    ModelSerializer,
    Serializer,
    SlugRelatedField,
    ValidationError,
)

from core.models import Livro
from uploader.models import Image
from uploader.serializers import ImageSerializer


class LivroAlterarPrecoSerializer(Serializer):  # noqa: E302
    preco = DecimalField(max_digits=7, decimal_places=2)

    def validate_preco(self, value):
        '''Valida se o preço é um valor positivo.'''
        if value <= 0:
            raise ValidationError('O preço deve ser um valor positivo.')
        return value

class LivroSerializer(ModelSerializer):  # noqa: E302
    capa_attachment_key = SlugRelatedField(
        source='capa',
        queryset=Image.objects.all(),
        slug_field='attachment_key',
        required=False,
        write_only=True,
    )
    capa = ImageSerializer(required=False, read_only=True)

    class Meta:
        model = Livro
        fields = "__all__"
        depth = 1


class LivroListRetrieveSerializer(ModelSerializer):
    capa = ImageSerializer(required=False)
    class Meta:
        model = Livro
        fields = "__all__"
        depth = 1

class LivroListSerializer(ModelSerializer):  # noqa: E302
    class Meta:
        model = Livro
        fields = ("id", "titulo", "preco")


class LivroMaisVendidoSerializer(ModelSerializer):
    total_vendidos = IntegerField()  # noqa: F821

    class Meta:
        model = Livro
        fields = ['id', 'titulo', 'total_vendidos']

class LivroRetrieveSerializer(ModelSerializer):  # noqa: E302
    capa = ImageSerializer(required=False)

    class Meta:
        model = Livro
        fields = '__all__'
        depth = 1
