from rest_framework.serializers import ModelSerializer, SerializerMethodField

from core.models import Compra, ItensCompra


class ItensCompraCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = ItensCompra
        fields = ('livro', 'quantidade')


class CompraCreateUpdateSerializer(ModelSerializer):
    itens = ItensCompraCreateUpdateSerializer(many=True)

    class Meta:
        model = Compra
        fields = ('usuario', 'itens')

        def create(self, validated_data):
            itens_data = validated_data.pop('itens')
            compra = Compra.objects.create(**validated_data)
            for item_data in itens_data:
                ItensCompra.objects.create(compra=compra, **item_data)
            compra.save()
            return compra


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
        fields = ('id', 'usuario', 'status', 'total', 'itens')

    @property
    def total(self):
        # total = 0
        # for item in self.itens.all():
        #     total += item.livro.preco * item.quantidade
        # return total
        return sum(item.livro.preco * item.quantidade for item in self.itens.all())
