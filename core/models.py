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

# Create your models here.
