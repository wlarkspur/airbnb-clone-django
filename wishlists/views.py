from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rooms.models import Room
from .models import Wishlist
from .serializers import WishListSerilaizer


class WishLists(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_wishlists = Wishlist.objects.filter(user=request.user)
        serializer = WishListSerilaizer(
            all_wishlists,
            many=True,
            context={
                "request": request,
            },
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = WishListSerilaizer(data=request.data)
        if serializer.is_valid():
            wishlist = serializer.save(
                user=request.user,
            )
            serializer = WishListSerilaizer(wishlist)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WishListDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishListSerilaizer(
            wishlist,
            context={"request": request},
        )
        return Response(serializer.data)

    def delete(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        wishlist.delete()
        return Response(status=HTTP_200_OK)

    def put(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishListSerilaizer(
            wishlist,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            wishlist = serializer.save()
            serializer = WishListSerilaizer(wishlist)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WishListToggle(APIView):
    def get_list(self, pk, user):
        try:
            return Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise NotFound

    def get_room(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def put(self, request, pk, room_pk):
        wishlist = self.get_list(pk, request.user)
        room = self.get_room(room_pk)
        if wishlist.rooms.filter(pk=room.pk).exists():
            # .exists()가 있으면 TRUE,FALSE 값을 받고, 아니면 list값을 받는다.
            wishlist.rooms.remove(room)
        else:
            wishlist.rooms.add(room)
        return Response(status=HTTP_200_OK)
