from typing import Any
import strawberry
import typing
from strawberry.types.info import Info
from . import types
from . import queries
from strawberry.permission import BasePermission
from common.permissions import OnlyLoggedIn
from .mutations import create_room


@strawberry.type
class Query:
    all_rooms: typing.List[types.RoomType] = strawberry.field(
        resolver=queries.get_all_rooms,
        permission_classes=[OnlyLoggedIn],
    )
    room: typing.Optional[types.RoomType] = strawberry.field(
        resolver=queries.get_room,
    )


@strawberry.type
class Mutation:
    create_room: types.RoomType = strawberry.mutation(
        resolver=create_room,
        permission_classes=[OnlyLoggedIn],
    )
