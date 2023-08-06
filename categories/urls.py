from django.urls import path
from . import views

urlpatterns = [
    path("", views.Categories.as_view()),
    path("<int:pk>", views.CategoryDetail.as_view()),
]

"""as_view: 하나의 규칙으로 GET, PUT 요청에 따라 코드를 실행하는 역할을 한다."""
