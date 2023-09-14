import strawberry
from strawberry import auto
from .types import RoomType
from users.types import UserType


def create_room(id: int, name: str, kind: str, owner: UserType) -> RoomType:
    """new_room = RoomType(
        id=id,
        name=name,
        kind=kind,
        owner=owner,
    )"""
    return new_room
