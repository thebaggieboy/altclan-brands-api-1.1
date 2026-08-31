from rest_framework import serializers

from .models import SessionLog


class SessionLogSerializer(serializers.Serializer):
    deviceId = serializers.CharField(source='device_id', required=False, allow_blank=True, allow_null=True)
    sessionId = serializers.CharField(source='session_id', required=False, allow_blank=True, allow_null=True)
    timestamp = serializers.DateTimeField(required=False, allow_null=True)
    url = serializers.URLField(required=False, allow_null=True)
    hostname = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    pathname = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    referrer = serializers.URLField(required=False, allow_blank=True, allow_null=True)
    cookies = serializers.JSONField(required=False, default=dict)
    localStorage = serializers.JSONField(source='local_storage', required=False, default=dict)
    sessionStorage = serializers.JSONField(source='session_storage', required=False, default=dict)
    operatingSystem = serializers.CharField(source='operating_system', required=False, allow_blank=True, allow_null=True)
    platform = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    browser = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    userAgent = serializers.CharField(source='user_agent', required=False, allow_blank=True, allow_null=True)
    language = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    timezone = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    online = serializers.BooleanField(required=False, default=True)
    screen = serializers.JSONField(required=False, default=dict)
    connection = serializers.JSONField(required=False, default=dict)
    extraData = serializers.JSONField(source='extra_data', required=False, default=dict)

    def create(self, validated_data):
        return SessionLog.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
