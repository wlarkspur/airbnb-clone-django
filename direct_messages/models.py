from django.db import models
from common.models import CommonModel
from config import settings


class ChattingRoom(CommonModel):

    """Room Model Definition"""

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
    )

    def __str__(self) -> str:
        return "Chatting Room"


class Message(CommonModel):

    """MEssage Model Definition"""

    text = models.TextField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="messages",
    )
    room = models.ForeignKey(
        "direct_messages.ChattingRoom",
        on_delete=models.CASCADE,
        related_name="messages",
    )

    def __str__(self) -> str:
        return f"{self.user} says: {self.text}"
