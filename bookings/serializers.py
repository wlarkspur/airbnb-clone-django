from rest_framework.serializers import ModelSerializer
from .models import Booking


# 일반 User를 위한 Public BookingSerializer 와 Owner를 위한 Serializer가 필요하다.
class PublicBookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "experience_time",
            "guests",
        )
