from rest_framework.serializers import (
    CharField,
    CurrentUserDefault,
    DateTimeField,  # novo campo
    HiddenField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
)

from core.models import Compra, ItensCompra


class ItensCompraCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = ItensCompra
        fields = ('livro', 'quantidade', 'preco')

    def validate_quantidade(self, quantidade):
        if quantidade <= 0:
            raise ValidationError('A quantidade deve ser maior do que zero.')
        return quantidade

    def validate(self, item):
        if item['quantidade'] > item['livro'].quantidade:
            raise ValidationError(
                (
                    f'Você tentou comprar {item["quantidade"]} unidades mas só temos '
                    f'{item["livro"].quantidade} unidades em estoque.'
                )
            )
        return item


class CompraCreateUpdateSerializer(ModelSerializer):
    usuario = HiddenField(default=CurrentUserDefault())
    itens = ItensCompraCreateUpdateSerializer(many=True)

    class Meta:
        model = Compra
        fields = ('usuario', 'itens')

    def create(self, validated_data):
        itens_data = validated_data.pop('itens')
        compra = Compra.objects.create(**validated_data)
        for item_data in itens_data:
            item_data['preco'] = item_data['livro'].preco  # preço do livro no momento da compra
            ItensCompra.objects.create(compra=compra, **item_data)
        compra.save()
        return compra

    def update(self, compra, validated_data):
        itens_data = validated_data.pop('itens', [])
        if itens_data:
            compra.itens.all().delete()
            for item_data in itens_data:
                item_data['preco'] = item_data['livro'].preco  # preço do livro no momento da compra
                ItensCompra.objects.create(compra=compra, **item_data)
        return super().update(compra, validated_data)


class ItensCompraListSerializer(ModelSerializer):
    livro = CharField(source='livro.titulo', read_only=True)

    class Meta:
        model = ItensCompra
        fields = (
            'livro',
            'quantidade',
            'preco',
        )
        # depth = 1


class CompraListSerializer(ModelSerializer):
    usuario = CharField(source='usuario.email', read_only=True)
    itens = ItensCompraListSerializer(many=True, read_only=True)

    class Meta:
        model = Compra
        fields = ('id', 'usuario', 'itens')


class ItensCompraSerializer(ModelSerializer):
    total = SerializerMethodField()

    def get_total(self, item):
        return item.preco * item.quantidade

    class Meta:
        model = ItensCompra
        fields = ('quantidade', 'preco', 'total', 'livro')
        depth = 2


class CompraSerializer(ModelSerializer):
    usuario = CharField(source='usuario.email', read_only=True)
    status = CharField(source='get_status_display', read_only=True)
    tipo_pagamento = CharField(source='get_tipo_pagamento_display', read_only=True)
    data = DateTimeField(read_only=True)  # novo campo
    itens = ItensCompraSerializer(many=True, read_only=True)

    class Meta:
        model = Compra
        fields = ('id', 'usuario', 'status', 'tipo_pagamento', 'data', 'total', 'itens')
