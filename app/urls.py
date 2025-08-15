from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.routers import DefaultRouter

from core.views import (
    CategoriaViewSet,
    CompraViewSet,  # inclua essa linha
    EditoraViewSet,
    UserViewSet,
)
from uploader.router import router as uploader_router

router = DefaultRouter()
router.register(r"categorias", CategoriaViewSet)  # nova linha
router.register(r"editoras", EditoraViewSet)
router.register(r"users", UserViewSet, basename="users")
router.register(r'compras', CompraViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    # OpenAPI 3
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'api/swagger/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
    path(
        'api/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc',
    ),
    # Uploader
    path("api/media/", include(uploader_router.urls)),  # nova linha
    # API
    path('api/', include(router.urls)),
]
urlpatterns += static(settings.MEDIA_ENDPOINT, document_root=settings.MEDIA_ROOT)
