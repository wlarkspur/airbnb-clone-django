from django.urls import path
from .views import WishLists, WishListDetail, WishListToggle


urlpatterns = [
    path("", WishLists.as_view()),
    path("<int:pk>", WishListDetail.as_view()),
    path("<int:pk>/rooms/<int:room_pk>", WishListToggle.as_view()),
]
