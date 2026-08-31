from django.db import models
from django.conf import settings


class TrackingEvent(models.Model):
	EVENT_TYPES = [
		('impression', 'Impression'),
		('click', 'Click'),
	]

	event_type = models.CharField(max_length=32, choices=EVENT_TYPES)
	item_id = models.CharField(max_length=128, null=True, blank=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
	metadata = models.JSONField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.event_type} {self.item_id} @ {self.created_at.isoformat()}"


class SessionLog(models.Model):
    device_id = models.CharField(max_length=255, blank=True, null=True)
    session_id = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    url = models.URLField(max_length=2048, blank=True, null=True)
    hostname = models.CharField(max_length=255, blank=True, null=True)
    pathname = models.CharField(max_length=2048, blank=True, null=True)
    referrer = models.URLField(max_length=2048, blank=True, null=True)
    cookies = models.JSONField(default=dict, blank=True)
    local_storage = models.JSONField(default=dict, blank=True)
    session_storage = models.JSONField(default=dict, blank=True)
    operating_system = models.CharField(max_length=255, blank=True, null=True)
    platform = models.CharField(max_length=255, blank=True, null=True)
    browser = models.CharField(max_length=255, blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=255, blank=True, null=True)
    timezone = models.CharField(max_length=255, blank=True, null=True)
    online = models.BooleanField(default=True)
    screen = models.JSONField(default=dict, blank=True)
    connection = models.JSONField(default=dict, blank=True)
    extra_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"SessionLog {self.device_id or self.session_id or self.id}"
