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


class UsageStatisticsSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()
    last_hour_clicks = serializers.IntegerField(read_only=True)
    last_day_clicks = serializers.IntegerField(read_only=True)

    class Meta:
        model = Link
        fields = ['link', 'original_link', 'last_hour_clicks', 'last_day_clicks']
        read_only_fields = fields

    def get_link(self, obj):
        request = self.context.get('request')
        if request and obj.short_link:
            return request.build_absolute_uri(f'/r/{obj.short_link}')
        return f'/r/{obj.short_link}' if obj.short_link else None
