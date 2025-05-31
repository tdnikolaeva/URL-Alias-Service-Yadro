import random
import string
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, status, mixins
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import Link, Usage
from .serializers import LinkSerializer


class LinkViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination

    def _generate_short_link(self, length=10):
        alphabet = string.ascii_letters + string.digits
        while True:
            short_link = ''.join(random.choices(alphabet, k=length))
            if not Link.objects.filter(short_link=short_link).exists():
                return short_link

    def perform_create(self, serializer):
        short_link = self._generate_short_link()
        serializer.save(short_link=short_link)

    @extend_schema(
        responses={
            status.HTTP_204_NO_CONTENT: None,
        },
    )
    @action(detail=True, methods=['patch'])
    def deactivate(self, request, pk=None):
        link = self.get_object()
        link.is_active = False
        link.save()
        return Response(status=status.HTTP_204_NO_CONTENT)



