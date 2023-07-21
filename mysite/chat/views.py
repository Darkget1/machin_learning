from django.shortcuts import render

from chat.models import Room,Message


def index_view(request):
    return render(request, 'chat/index.html', {
        'rooms': Room.objects.all(),
    })


def room_view(request, room_name):
    room_id = Room.objects.get(name=room_name)
    message_list = Message.objects.filter(room_id=room_id)
    chat_room, created = Room.objects.get_or_create(name=room_name)
    return render(request, 'chat/room.html', {
        'room': chat_room,'message_list':message_list,
    })
