from django.db import models
from django.utils import timezone
from datetime import timedelta


class Link(models.Model):
    original_link = models.URLField()
    short_link = models.CharField(max_length=10, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(days=1)

    @property
    def is_valid(self):
        return self.is_active and not self.is_expired


class Usage(models.Model):
    link = models.ForeignKey(
        Link,
        on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField(auto_now_add=True)
