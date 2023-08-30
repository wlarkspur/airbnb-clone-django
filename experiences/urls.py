from django.urls import path
from .views import Perks, PerkDetail
from . import views


urlpatterns = [
    path("", views.ExperiencesList.as_view()),
    path("<int:pk>", views.ExperiencesDetail.as_view()),
    path("perks/", Perks.as_view()),
    path("perks/<int:pk>", PerkDetail.as_view()),
]
