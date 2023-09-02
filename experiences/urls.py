from django.urls import path
from .views import Perks, PerkDetail
from . import views


urlpatterns = [
    path("", views.ExperiencesList.as_view()),
    path("<int:pk>", views.ExperiencesDetail.as_view()),
    path("<int:pk>/perks", views.ExperiencesPerks.as_view()),
    path("<int:pk>/bookings", views.ExperiencesBookings.as_view()),
    path("<int:pk>/bookings/<int:exp_pk>", views.ExperiencesBookingsDetail.as_view()),
    path("perks/", Perks.as_view()),
    path("perks/<int:pk>", PerkDetail.as_view()),
]
