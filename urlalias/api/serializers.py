from rest_framework import serializers
from .models import Link, Usage


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['id', 'original_link', 'short_link', 'is_active', 'created_at']
        read_only_fields = ['short_link', 'is_active', 'created_at']


class UsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usage
        fields = ['timestamp']
