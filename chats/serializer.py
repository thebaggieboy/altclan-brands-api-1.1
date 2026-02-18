from rest_framework import serializers
from .models import ChatRoom, Message


class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.EmailField(source='sender.email', read_only=True)
    sender_name = serializers.CharField(source='sender.get_full_name', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'room', 'sender', 'sender_email', 'sender_name', 'content', 'timestamp']
        read_only_fields = ['id', 'sender', 'sender_email', 'sender_name', 'timestamp']


class ChatRoomSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    participant_emails = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'participants', 'participant_emails', 'created_at', 'last_message']
        read_only_fields = ['id', 'created_at']

    def get_last_message(self, obj):
        last_msg = obj.messages.order_by('-timestamp').first()
        if last_msg:
            return {
                'content': last_msg.content,
                'sender_email': last_msg.sender.email,
                'timestamp': last_msg.timestamp.isoformat(),
            }
        return None

    def get_participant_emails(self, obj):
        return list(obj.participants.values_list('email', flat=True))
