from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LinkViewSet, UsagesViewSet, ShortLinkViewSet

router = DefaultRouter()
router.register(r'links', LinkViewSet, basename='links')
router.register(r'statistics', UsagesViewSet, basename='statistics')
router.register(r'', ShortLinkViewSet, basename='redirect')

urlpatterns = [
    path('', include(router.urls)),
]
