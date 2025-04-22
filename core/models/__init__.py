from .user import User
from .categoria import Categoria

from .editora import Editora
from .autor import Autor
from .livro import Livro

class Livro(models.Model):
    titulo = models.CharField(max_length=255)
    isbn = models.CharField(max_length=32, null=True, blank=True)
    quantidade = models.IntegerField(default=0,  null=True, blank=True)
    preco = models.DecimalField(max_digits=7, decimal_places=2, default=0, null=True, blank=True)
    from .categoria import Categoria
    categoria = models.ForeignKey(
        Categoria, on_delete=models.PROTECT, related_name="livros", null=True, blank=True
    )
    from .editora import Editora
    editora = models.ForeignKey(Editora, on_delete=models.PROTECT, related_name="livros", null=True, blank=True)
    def __str__(self):
        return f"({self.id}) {self.titulo} ({self.quantidade})"