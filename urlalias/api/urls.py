from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LinkViewSet

router = DefaultRouter()
router.register(r'links', LinkViewSet, basename='links')
# router.register(r'statistics', StatisticsViewSet, basename='statistics')  # если реализуете статистику

urlpatterns = [
    path('', include(router.urls)),

    # path('r/<str:short_link>/', RedirectView.as_view(), name='redirect'),
]