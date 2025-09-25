from .user import UserSerializer
from .categoria import CategoriaSerializer
from .editora import EditoraSerializer
from .livro import LivroSerializer
from .livro import LivroListRetrieveSerializer, LivroSerializer
from .compra import (
    CompraCreateUpdateSerializer,
    CompraListSerializer, # novo
    CompraSerializer,
    ItensCompraCreateUpdateSerializer,
    ItensCompraListSerializer, # novo
    ItensCompraSerializer,
)