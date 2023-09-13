from strawberry.types import Info
from . import models


""" def get_all_rooms(info: Info):
    if info.context.request.user.is_authenticated:
        return models.Room.objects.all()
    else:
        raise Exception("Not auth.") """


def get_all_rooms():
    return models.Room.objects.all()


def get_room(pk: int):
    try:
        return models.Room.objects.get(pk=pk)
    except models.Room.DoesNotExist:
        return None
