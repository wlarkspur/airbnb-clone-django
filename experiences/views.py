from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status
from .models import Perk, Experiences
from .serializers import (
    PerkSerializer,
    ExperiencesListSerializer,
    ExperiencesDetailSerializer,
)


class ExperiencesList(APIView):
    def get(self, request):
        all_experiences = Experiences.objects.all()
        serializer = ExperiencesListSerializer(
            all_experiences,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = ExperiencesListSerializer(data=request.data)
        if serializer.is_valid():
            experience = serializer.save()
            serializer = ExperiencesListSerializer(experience)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class ExperiencesDetail(APIView):
    def get_object(self, pk):
        try:
            return Experiences.objects.get(pk=pk)
        except Experiences.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experiences = self.get_object(pk)
        serializer = ExperiencesDetailSerializer(
            experiences, context={"request": request}
        )
        return Response(serializer.data)

    def put(self, request, pk):
        experience = self.get_object(pk)
        serializer = ExperiencesDetailSerializer(
            experience, data=request.data, partial=True
        )
        if serializer.is_valid():
            updated_experience = serializer.save()
            serializer = ExperiencesDetailSerializer(
                updated_experience, context={"request": request}
            )
            # serializer.py의 get_is_owner에서 request key를 받고 있었기 때문에 이곳에서도 context={"request":request}값을 추가해줘야 한다.
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        experience = self.get_object(pk)
        experience.delete()
        return Response(status=status.HTTP_200_OK)


class ExperiencesPerks(APIView):
    pass


class Perks(APIView):
    def get(self, request):
        all_perks = Perk.objects.all()
        serializer = PerkSerializer(all_perks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PerkSerializer(data=request.data)
        if serializer.is_valid():
            perk = serializer.save()
            return Response(PerkSerializer(perk).data)
        else:
            return Response(serializer.errors)


class PerkDetail(APIView):
    def get_object(self, pk):
        try:
            return Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        perk = self.get_object(pk)
        serializer = PerkSerializer(perk)
        return Response(serializer.data)

    def put(self, request, pk):
        perk = self.get_object(pk)
        serializer = PerkSerializer(perk, data=request.data, partial=True)
        if serializer.is_valid():
            updated_perk = serializer.save()
            return Response(
                PerkSerializer(updated_perk).data,
            )
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(status=HTTP_204_NO_CONTENT)
