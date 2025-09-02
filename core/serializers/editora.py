import email  # noqa: F401, I001
from rest_framework.serializers import ModelSerializer

from core.models import Editora


class EditoraSerializer(ModelSerializer):
    class Meta:
        model = Editora
        fields = "__all__"

    def validate_email(self, email):  # noqa: E113, E301, E305, F811
        return email.lower()  # noqa: E117
