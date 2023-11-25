import time
from django.conf import settings
from django.db import transaction
from django.http import Http404
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_204_NO_CONTENT,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    ParseError,
    PermissionDenied,
)
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from medias.models import Photo
from .models import Amenity, Room
from categories.models import Category
from .serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from bookings.models import Booking
from bookings.serializers import PublicBookingSerializer, CreateRoomBookingSerializer


class Amenities(APIView):
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(
                AmenitySerializer(amenity).data,
            )
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(
            amenity,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(
                AmenitySerializer(updated_amenity).data,
            )
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )

    """ 
    put 코드: 
    1. amenity에서 기존DB의 데이터를 가져온다
    2. serializer를 이용하여 amenity의 유저 data를 가져오고 partial 옵션으로 일부 수정가능 하도록 해준다.

    """

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Rooms(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(
            all_rooms,
            many=True,
            context={
                "request": request,
            },
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = RoomDetailSerializer(data=request.data)
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if not category_pk:
                raise ParseError("Category is required.")
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == category.CategoryKindChoices.EXPERIENCES:
                    raise ParseError("The category kind should be rooms")
            except Category.DoesNotExist:
                raise ParseError("Category not found")
            try:
                with transaction.atomic():
                    room = serializer.save(
                        owner=request.user,
                        category=category,
                    )
                    amenities = request.data.get("amenities")
                    for amenity_pk in amenities:
                        amenity = Amenity.objects.get(pk=amenity_pk)
                        room.amenities.add(amenity)
                    serializer = RoomDetailSerializer(
                        room,
                        context={"request": request},
                    )
                    return Response(serializer.data)
            except Category.DoesNotExist:
                raise ParseError("Amenity not found")
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class RoomDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_objects(self, pk):
        """time.sleep(1)"""
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_objects(pk)
        serializer = RoomDetailSerializer(
            room,
            context={
                "request": request,
            },
        )
        return Response(serializer.data)

    def put(self, request, pk):
        room = self.get_objects(pk)
        if room.owner != request.user:
            raise PermissionDenied
        serializer = RoomDetailSerializer(
            room,
            data=request.data,
            partial=True,
        )
        # amenities, category 는 read_only 이므로 데이터를 가져와야 한다.
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if not request.data.get("category"):
                raise ParseError("category is required")
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                    raise ParseError("category should be rooms")
            except Category.DoesNotExist:
                raise ParseError(f"Category id not found")
            # <----- 여기 진행중
            try:
                with transaction.atomic():
                    if category_pk:
                        room = serializer.save(category=category)
                    else:
                        room = serializer.save()
                    amenities = request.data.get("amenities")
                    if amenities:
                        room.amenities.clear()
                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            print(amenity)
                            room.amenities.add(amenity)
                        serializer = AmenitySerializer(room)
                        return Response(serializer.data)
                    else:
                        return Response(serializer.errors)
            except Amenity.DoesNotExist:
                raise ParseError(f"amenity id not found")
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        room = self.get_objects(pk)
        if room.owner != request.user:
            raise PermissionDenied
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class RoomReviews(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = 3
        start = (page - 1) * page_size
        end = start + page_size
        room = self.get_object(pk)
        serializer = ReviewSerializer(
            room.reviews.all()[start:end],
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(
                user=request.user,
                room=self.get_object(pk),
            )
            serializer = ReviewSerializer(review)
            return Response(serializer.data)


class RoomAmenities(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        room = self.get_object(pk)
        serializer = AmenitySerializer(
            room.amenities.all()[start:end],
            many=True,
        )
        return Response(serializer.data)


class RoomPhotos(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk=pk)
        if request.user != room.owner:
            raise PermissionDenied
        all_photos = Photo.objects.all()
        serializer = PhotoSerializer(
            all_photos,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        room = self.get_object(pk)
        if request.user != room.owner:
            raise PermissionDenied
        # 유저 인증 여부 & room의 오너인지 확인
        serializer = PhotoSerializer(data=request.data)
        # request.data를 파이썬 Object로 넘기는 과정
        if serializer.is_valid():
            photo = serializer.save(room=room)
            # 사진을 저장할 때 사진이 속한 room도 같이 보내야 한다.
            serializer = PhotoSerializer(photo)
            # 파이썬 Object를 JSON으로 넘기는 과정
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def put(self, request, pk):
        room = self.get_object(pk)
        if request.user != room.owner:
            raise PermissionDenied

        photo_pk = request.data.get("pk")
        print(photo_pk, request.data)
        photo = get_object_or_404(Photo, pk=photo_pk, room=room)
        print("aaa=>", photo)
        serializer = PhotoSerializer(
            photo,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_photo = serializer.save()
            return Response(PhotoSerializer(updated_photo).data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class RoomBookings(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    # 모든 User가 Get요청을 받을순 있지만, Put, Post, Delete Method는 인증된 User만 사용할 수 있다.

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = 5
        start = (page - 1) * page_size
        end = start + page_size
        room = self.get_object(pk)
        now = timezone.localtime(timezone.now()).date()
        bookings = Booking.objects.filter(
            room=room,
            kind=Booking.BookingKindChoices.ROOM,
            check_in__gt=now,
        )
        serializer = PublicBookingSerializer(
            room.bookings.all()[start:end],
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        room = self.get_object(pk)
        serializer = CreateRoomBookingSerializer(
            data=request.data,
            context={"room": room},
        )
        if serializer.is_valid():
            booking = serializer.save(
                room=room,
                user=request.user,
                kind=Booking.BookingKindChoices.ROOM,
            )
            serializer = PublicBookingSerializer(booking)
            # check_in = request.data.get("check_in")
            # 유저가 보낸 date가 미래 날짜가 아닐때 false 반환하도록 하는 방법
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class RoomBookingCheck(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        check_out = request.query_params.get("check_out")
        check_in = request.query_params.get("check_in")
        # query_params 는 주소 ?abc=abc 같은 식으로 주소를 나타낸다
        exists = Booking.objects.filter(
            room=room,
            check_in__lt=check_out,
            check_out__gt=check_in,
        ).exists()
        if exists:
            return Response({"ok": False})
        return Response({"ok": True})
