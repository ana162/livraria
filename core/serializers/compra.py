from rest_framework.serializers import CharField, ModelSerializer, SerializerMethodField  # noqa: I001

from core.models import Compra, ItensCompra, compra

from rest_framework.serializers import (
    CharField,  # noqa: F811
    CurrentUserDefault,  # novo  # noqa: F401
    DateTimeField, # novo  # noqa: E261, F401
    HiddenField,         # novo  # noqa: F401
    ModelSerializer,  # noqa: F811
    SerializerMethodField,  # noqa: F811
    ValidationError, # novo  # noqa: E261, F401
)


class ItensCompraCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = ItensCompra
        fields = ('livro', 'quantidade', 'preco')  # mudou

    def validate_quantidade(self, quantidade):
        if quantidade <= 0:
            raise ValidationError('A quantidade deve ser maior do que zero.')
        return quantidade

    def validate(self, item):  # noqa: F811
        if item['quantidade'] > item['livro'].quantidade:
            raise ValidationError('Quantidade de itens maior do que a quantidade em estoque.')
        return item


class CompraCreateUpdateSerializer(ModelSerializer):
    usuario = HiddenField(default=CurrentUserDefault())
    itens = ItensCompraCreateUpdateSerializer(many=True)

    class Meta:
        model = Compra  # noqa: E111
        fields = ('usuario', 'itens')

    def update(self, compra, validated_data):  # noqa: E305
        itens = validated_data.pop('itens',[])  # noqa: E117, E231
        if itens:
            compra.itens.all().delete()
            for item in itens:  # noqa: E117
                item['preco'] = item['livro'].preco
                ItensCompra.objects.create(compra=compra, **item)  # noqa: F821

        return super().update(compra, validated_data)

    def create(self, validated_data):
        compra.save()  # linha adicionada para salvar a compra  # noqa: F823
        return compra  # noqa: E302

        itens = validated_data.pop('itens')  # noqa: E117
        usuario = validated_data['usuario']  # noqa: F841

        compra,criada = Compra.objects.get_or_create(  # noqa: E231
        usuario=usuario, status=Compra.StatusCompra.CARRINHO, defaults=validated_data  # noqa: E225
        )

        for item in itens:  # noqa: F402
            item_existente = compra.itens.filter(livro=item['livro']).first()

            if item_existente:
                item_existente.quantidade += item['quantidade']
                item_existente.preco = item['livro'].preco
                item_existente.save()
            else:
                item['preco'] = item['livro'].preco
            ItensCompra.objects.create(compra=compra, **item)
        compra.save()
        return compra

class ItensCompraSerializer(ModelSerializer):  # noqa: E302
    total = SerializerMethodField()

    def get_total(self, instance):
        return instance.quantidade * instance.preco

    class Meta:
        model = ItensCompra
        fields = ('quantidade', 'preco', 'total', 'livro')
        depth = 2


class CompraSerializer(ModelSerializer):
    usuario = CharField(source='usuario.email', read_only=True)  # noqa: E117
    status = CharField(source='get_status_display', read_only=True)
    data = DateTimeField(read_only=True) # novo campo  # noqa: E261
    tipo_pagamento = CharField(source='get_tipo_pagamento_display', read_only=True) # novo campo  # noqa: E261
    itens = ItensCompraSerializer(many=True, read_only=True)

    class Meta:
        model = Compra  # noqa: E117
        fields = ('id', 'usuario', 'status', 'total', 'data', 'tipo_pagamento', 'itens') # modificado  # noqa: E261

class ItensCompraListSerializer(ModelSerializer):  # noqa: E302
    total = SerializerMethodField()

    def get_total(self, instance):
        return instance.livro.preco * instance.quantidade

    class Meta:
        model = ItensCompra
        fields = ('quantidade', 'preco', 'livro')  # mudou
        depth = 1
  # noqa: E114, W293
class CompraListSerializer(ModelSerializer):  # noqa: E302
    usuario = CharField(source='usuario.email', read_only=True)  # noqa: F821
    itens = ItensCompraListSerializer(many=True, read_only=True)
    class Meta:
        model = Compra
        fields = ('id', 'usuario', 'itens')


class ItensCompraListSerializer(ModelSerializer):
    livro = CharField(source='livro.titulo', read_only=True)

    class Meta:
        model = ItensCompra
        fields = ('quantidade', 'preco', 'livro')  # mudou
        depth = 1

    @property
    def total(self):
        # total = 0
        # for item in self.itens.all():
        #     total += item.livro.preco * item.quantidade
        # return total
        return sum(item.livro.preco * item.quantidade for item in self.itens.all())  # noqa: F811
