from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category
from .serializers import CategorySerializer

""" all_categories 는 Queryset으로 JsonResponse를 통해 Json값이 아닌 Queryset 값을 주게된다
그러면, 브라우저는 Queryset을 이해하지 못하기 때문에 오류가 발생한다. 대신 JSON 포맷으로 변경필요 """


@api_view(["GET", "POST"])
def categories(request):
    if request.method == "GET":
        all_categories = Category.objects.all()
        serializer = CategorySerializer(all_categories, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = CategorySerializer(data=request.data)
        return Response({"created": True})


@api_view()
def category(request, pk):
    category = Category.objects.get(pk=pk)
    serializer = CategorySerializer(category)
    return Response(serializer.data)
