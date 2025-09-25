from django.db import models


class Editora(models.Model):
    nome = models.CharField(max_length=100)
    site = models.URLField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
      return f"({self.id}) {self.nome}"  # noqa: E111


from .editora import Editora  # noqa: E402, F811

editora = models.ForeignKey(Editora, on_delete=models.PROTECT, related_name="livros", null=True, blank=True)
