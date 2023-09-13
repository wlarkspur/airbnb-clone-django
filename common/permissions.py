from strawberry.types import Info
import typing
from strawberry.permission import BasePermission


# 로그인 되지 않은 경우 아래 함수를 실행시킨다.
class OnlyLoggedIn(BasePermission):
    message = "You need to be logged in for this!"

    def has_permission(self, source: typing.Any, info: Info):
        return info.context.request.user.is_authenticated
