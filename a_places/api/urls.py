from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import (
    WorkplaceViewSet,
    ReservationViewSet,
    UserViewSet,
    CreateReservationView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()

router.register(r'workplaces', WorkplaceViewSet)
router.register(r'users', UserViewSet)
router.register(r'reservations', ReservationViewSet, 'reservation')

urlpatterns = [
    re_path(r'^$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', include(router.urls)),
    path('workplaces/<int:pk>/reserve/', CreateReservationView.as_view()),
    path('', include('rest_framework.urls', namespace='rest_framework')),
]
