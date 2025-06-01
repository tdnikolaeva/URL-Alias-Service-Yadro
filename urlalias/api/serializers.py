from rest_framework import serializers
from .models import Link


class LinkSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()

    class Meta:
        model = Link
        fields = ['id', 'original_link', 'link', 'is_active', 'created_at']
        read_only_fields = ['id', 'link', 'is_active', 'created_at']

    def get_link(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'/{obj.short_link}')
        return f'/{obj.short_link}'


class UsageStatisticsSerializer(serializers.Serializer):
    link = serializers.SerializerMethodField()
    original_link = serializers.URLField()
    last_hour_clicks = serializers.IntegerField()
    last_day_clicks = serializers.IntegerField()

    def get_link(self, link_obj):
        request = self.context.get('request')
        short_link = getattr(link_obj, 'short_link', None)
        if short_link and request:
            return request.build_absolute_uri(f'/{short_link}')
        return f'/{short_link}' if short_link else None
