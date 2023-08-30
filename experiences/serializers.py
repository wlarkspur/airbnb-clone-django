from rest_framework.serializers import ModelSerializer
from .models import Perk, Experiences
from users.serializers import TinyUserSerializer


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

    class Meta:
        model = Experiences
        fields = "__all__"
