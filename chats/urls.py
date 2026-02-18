from django.urls import path
from .views import ChatRoomList, MessageList, CreateChatRoom, SendMessage

urlpatterns = [
    path('rooms/', ChatRoomList.as_view(), name='chat-room-list'),
    path('rooms/create/', CreateChatRoom.as_view(), name='chat-room-create'),
    path('rooms/<str:room_name>/messages/', MessageList.as_view(), name='message-list'),
    path('rooms/<str:room_name>/messages/send/', SendMessage.as_view(), name='send-message'),
]
