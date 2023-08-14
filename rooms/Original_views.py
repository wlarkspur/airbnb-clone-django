from django.shortcuts import render
from django.http import HttpResponse
from .models import Room


# Create your views here.
def say_hello(request):
    return HttpResponse("Hello!")


def see_all_room(request):
    rooms = Room.objects.all()
    return render(
        request,
        "all_rooms.html",
        {
            "rooms": rooms,
            "title": "Hello! this title comes from django",
        },
    )


def see_one_room(request, room_pk):
    try:
        room = Room.objects.get(pk=room_pk)
        return render(
            request,
            "room_detail.html",
            {
                "room": room,
            },
        )
    except Room.DoesNotExist:
        return render(
            request,
            "room_detail.html",
            {
                "not_found": True,
            },
        )
