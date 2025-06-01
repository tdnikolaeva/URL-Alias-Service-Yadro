import random
import string
from datetime import timedelta
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Link, Usage
from .serializers import LinkSerializer, UsageStatisticsSerializer


class LinkViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active']

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


class UsagesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Usage.objects.all()
    serializer_class = UsageStatisticsSerializer
    pagination_class = None

    def list(self, request, *args, **kwargs):
        now = timezone.now()
        one_hour_ago = now - timedelta(hours=1)
        one_day_ago = now - timedelta(days=1)

        qs = self.queryset.annotate(
            last_hour_clicks=Count('usage', filter=Q(usage__timestamp__gte=one_hour_ago)),
            last_day_clicks=Count('usage', filter=Q(usage__timestamp__gte=one_day_ago)),
        ).order_by('-last_day_clicks')

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


class ShortLinkViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Link.objects.all()
    serializer_class = None
    permission_classes = [permissions.AllowAny]
    lookup_field = 'short_link'

    @extend_schema(
        responses={
            302: None
        }
    )
    def retrieve(self, request, *args, **kwargs):
        short_link = self.kwargs.get(self.lookup_field)
        link = get_object_or_404(Link, short_link=short_link)

        if not link.is_valid:
            return Response(
                {"detail": "Ссылка неактивна или устарела."},
                status=status.HTTP_400_BAD_REQUEST
            )

        Usage.objects.create(link=link)
        return redirect(link.original_link)
