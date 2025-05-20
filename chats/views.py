# views.py
from rest_framework import generics
from .models import Message, ChatRoom
from .serializers import MessageSerializer, ChatRoomSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageList(generics.ListAPIView):
    serializer_class = MessageSerializer
    
    def get_queryset(self):
        room_name = self.kwargs['room_name']
        return Message.objects.filter(room__name=room_name).order_by('timestamp')

class ChatRoomList(generics.ListAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    
    def get_queryset(self):
        return self.request.user.chat_rooms.all()