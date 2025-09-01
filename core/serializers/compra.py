from rest_framework.serializers import CharField, ModelSerializer, SerializerMethodField

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

    def update(self, compra, validated_data):
        itens_data = validated_data.pop('itens', [])
        if itens_data:
            compra.itens.all().delete()
            for item_data in itens_data:
                ItensCompra.objects.create(compra=compra, **item_data)
        return super().update(compra, validated_data)


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


class ItensCompraListSerializer(ModelSerializer):
    total = SerializerMethodField()

    def get_total(self, instance):
        return instance.livro.preco * instance.quantidade

    class Meta:
        model = ItensCompra
        fields = ('livro', 'quantidade', 'total')


class CompraListSerializer(ModelSerializer):
    usuario = CharField(source='usuario.email', read_only=True)  # noqa: F821
    itens = ItensCompraListSerializer(many=True, read_only=True)
    class Meta:
        model = Compra
        fields = ('id', 'usuario', 'itens')


class ItensCompraListSerializer(ModelSerializer):
    livro = CharField(source='livro.titulo', read_only=True)

    class Meta:
        model = ItensCompra
        fields = ('quantidade', 'livro')
        depth = 1

    @property
    def total(self):
        # total = 0
        # for item in self.itens.all():
        #     total += item.livro.preco * item.quantidade
        # return total
        return sum(item.livro.preco * item.quantidade for item in self.itens.all())
