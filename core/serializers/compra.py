from rest_framework.serializers import ModelSerializer, SerializerMethodField

from core.models import ItensCompra


class ItensCompraSerializer(ModelSerializer):
    total = SerializerMethodField()

    def get_total(self, instance):
        return instance.livro.preco * instance.quantidade


class CompraSerializer(ModelSerializer):
    class Meta:
        model = ItensCompra
        fields = ('livro', 'quantidade', 'total')
        depth = 1
        itens = ItensCompraSerializer(many=True, read_only=True)
