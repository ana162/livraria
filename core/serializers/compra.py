from rest_framework.serializers import ModelSerializer

from core.models import Compra, ItensCompra

class ItensCompraSerializer:
    def __init__(self, many=False, read_only=False):
        self.many = many
        self.read_only = read_only

class CompraSerializer(ModelSerializer):  
    class Meta:
        model = Compra
        fields= ('livro', 'quantidade')
        depth = 1
        itens = ItensCompraSerializer(many=True, read_only=True) 
