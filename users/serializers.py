from rest_framework.serializers import ModelSerializer
from .models import User
from rest_framework import serializers
from reviews.serializers import ReviewSerializer
from reviews.models import Review


class TinyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "name",
            "avatar",
            "username",
        )


class PrivateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "password",
            "is_superuser",
            "id",
            "is_staff",
            "is_active",
            "first_name",
            "last_name",
            "groups",
            "user_permissions",
        )


class PublicUserSerializer(ModelSerializer):
    reviews = serializers.SerializerMethodField()

    def get_reviews(self, user):
        reviews = Review.objects.filter(user=user)
        review_data = ReviewSerializer(reviews, many=True).data
        return review_data

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "name",
            "avatar",
            "gender",
            "groups",
            "reviews",
        )
