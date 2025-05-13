from .user import UserSerializer
from .categoria import CategoriaSerializer
from .editora import EditoraSerializer
from .livro import LivroListRetrieveSerializer, LivroSerializer

from core.serializers import LivroListRetrieveSerializer, LivroSerializer

class LivroViewSet(ModelViewSet):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return LivroListRetrieveSerializer
        return LivroSerializer