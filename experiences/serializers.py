from rest_framework.serializers import ModelSerializer
from .models import Perk, Experiences
from users.serializers import TinyUserSerializer
from rest_framework import serializers


class PerkSerializer(ModelSerializer):
    class Meta:
        model = Perk
        fields = (
            "id",
            "name",
            "details",
            "explanation",
        )


class ExperiencesListSerializer(ModelSerializer):
    class Meta:
        model = Experiences
        exclude = ("category",)


class ExperiencesDetailSerializer(ModelSerializer):
    perks = PerkSerializer(many=True)
    host = TinyUserSerializer()

    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Experiences
        fields = "__all__"

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.host == request.user
