from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Message, ChatRoom
from .serializer import MessageSerializer, ChatRoomSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatRoomList(generics.ListAPIView):
    """List all chat rooms for the authenticated user."""
    serializer_class = ChatRoomSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.request.user.chat_rooms.all().order_by('-created_at')
        return ChatRoom.objects.none()


class MessageList(generics.ListAPIView):
    """List all messages in a chat room by room name."""
    serializer_class = MessageSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        room_name = self.kwargs['room_name']
        return Message.objects.filter(room__name=room_name).order_by('timestamp')


class CreateChatRoom(generics.CreateAPIView):
    """Create a new chat room or return existing one between two users."""
    serializer_class = ChatRoomSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get('participant_ids', [])
        room_name = request.data.get('name', '')

        if not room_name:
            return Response(
                {'error': 'Room name is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if room already exists with this name
        existing_room = ChatRoom.objects.filter(name=room_name).first()
        if existing_room:
            serializer = self.get_serializer(existing_room)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Create new room
        room = ChatRoom.objects.create(name=room_name)

        # Add participants
        if request.user.is_authenticated:
            room.participants.add(request.user)

        for uid in participant_ids:
            try:
                user = User.objects.get(id=uid)
                room.participants.add(user)
            except User.DoesNotExist:
                pass

        serializer = self.get_serializer(room)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SendMessage(generics.CreateAPIView):
    """Send a message to a chat room via REST (fallback when WebSocket is unavailable)."""
    serializer_class = MessageSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        room_name = self.kwargs['room_name']
        content = request.data.get('content', '')

        if not content:
            return Response(
                {'error': 'Message content is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            room = ChatRoom.objects.get(name=room_name)
        except ChatRoom.DoesNotExist:
            return Response(
                {'error': 'Chat room not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        sender = request.user if request.user.is_authenticated else None
        if not sender:
            # For unauthenticated requests, try to get sender from request data
            sender_id = request.data.get('sender_id')
            if sender_id:
                try:
                    sender = User.objects.get(id=sender_id)
                except User.DoesNotExist:
                    pass

        if not sender:
            return Response(
                {'error': 'Authentication required to send messages'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        message = Message.objects.create(
            room=room,
            sender=sender,
            content=content
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)