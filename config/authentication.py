from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import User


class TrustMeAuthentication(BaseAuthentication):
    def authenticate(self, request):
        user = User.objects.get(username="admin")
        return (user, None)

        """ username = request.headers.get("Trust-Me")
        if not username:
            return None
        try:
            user = User.objects.get(username=username)
            return (user, None)  # (user,None)은 문법 규칙이다.
        except User.DoesNotExist:
            raise AuthenticationFailed(f"No user {username}")
 """
