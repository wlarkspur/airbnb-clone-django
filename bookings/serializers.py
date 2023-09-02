from django.utils import timezone
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Booking
from experiences.models import Experiences
from users.serializers import TinyUserSerializer


# 일반 User를 위한 Public BookingSerializer 와 Owner를 위한 Serializer가 필요하다.


class CreateRoomBookingSerializer(ModelSerializer):
    # serializers는 기본적으로 필수값으로 간주되며, 이를 원치않으면 (required=False)값으로 설정해줘야 한다.
    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "guests",
        )

    def validate_check_in(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        return value

    def validate_check_out(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now >= value:
            raise serializers.ValidationError("Can't book(check_out) in the past!")
        return value

    def validate(self, data):
        if data["check_out"] <= data["check_in"]:
            raise serializers.ValidationError(
                "It should check_in < check_out",
            )

        if Booking.objects.filter(
            check_in__lt=data["check_out"],
            check_out__gt=data["check_in"],
        ).exists():
            raise serializers.ValidationError(
                "Sorry, those dates are already booked :( "
            )
        return data


class PublicBookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "guests",
        )


class CreateExperienceBookingSerializer(ModelSerializer):
    experience_time = serializers.DateField()
    # is_owner = serializers.SerializerMethodField()
    """ user = TinyUserSerializer() """

    # model을 Booking에서 해야되나 ??
    class Meta:
        model = Booking
        fields = (
            "pk",
            "experience_time",
            "guests",
            # "is_owner",
        )

    def validate_experience_time(self, value):
        now = timezone.localtime(timezone.now()).date()
        if value < now:
            raise serializers.ValidationError("Can't not book in the past")

    def validate(self, data):
        if Booking.objects.filter(experience_time=data["experience_time"]).exists():
            raise serializers.ValidationError(
                "Sorry, that date is occupied :( select another date please"
            )


""" 
    def get_is_owner(self, experience):
        request = self.context["request"]
        return experience.user == request.user """

# request값은 Django에서 제공하는 값으로 일반적으로 user값은 User모델의 인스턴스이며, 로그인한 사용자의 정보를 저장 및 관리한다. 이외에도 request.path, request.get_host(), request.session, request.COOKIES 등 여러 값을 제공한다.


class PublicExperienceBookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "pk",
            "experience_time",
            "guests",
        )


class ExperienceBookingDetailSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "id",
            "guests",
            "experience_time",
            "check_in",
            "check_out",
            "user",
            "experience",
        )
