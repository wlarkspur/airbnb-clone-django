from rest_framework import serializers
from .models import Review
from users.models import User


class TinyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "name",
            "avatar",
            "username",
        )


class ReviewSerializer(serializers.ModelSerializer):
    user = TinyUserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = (
            "user",
            "payload",
            "rating",
            "room",
        )
