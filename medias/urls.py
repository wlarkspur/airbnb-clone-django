from django.urls import path
from .views import PhotoDetail, GetUpLoadURL

urlpatterns = [
    path("photos/get-url", GetUpLoadURL.as_view()),
    path("photos/<int:pk>", PhotoDetail.as_view()),
]
