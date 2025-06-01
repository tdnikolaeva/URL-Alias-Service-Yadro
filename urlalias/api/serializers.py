from rest_framework import serializers
from .models import Link, Usage


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['id', 'original_link', 'short_link', 'is_active', 'created_at']
        read_only_fields = ['short_link', 'is_active', 'created_at']


class UsageStatisticsSerializer(serializers.Serializer):
    link = serializers.CharField(source='short_link')
    original_link = serializers.URLField()
    last_hour_clicks = serializers.IntegerField()
    last_day_clicks = serializers.IntegerField()