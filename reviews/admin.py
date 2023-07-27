from django.contrib import admin
from .models import Review


class WordFilter(admin.SimpleListFilter):
    title = "Filter by words!"

    parameter_name = "word"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),
            ("great", "Great"),
            ("awesome", "Awesome"),
        ]

    def queryset(self, request, reviews):
        word = self.value()
        if word:
            return reviews.filter(payload__contains=word)
        else:
            return reviews


class CleanFilter(admin.SimpleListFilter):
    title = "Cleaner"

    parameter_name = "clean_word"

    def lookups(self, request, model_admin):
        return [
            ("bad", "Negative"),
            ("great", "Positive"),
        ]

    def queryset(self, request, reviews):
        clean = self.value()
        if clean == "bad":
            return reviews.filter(rating__lte=3)
        else:
            return reviews.filter(rating__gt=3)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "payload",
        "room",
        "experience",
    )
    list_filter = (
        CleanFilter,
        WordFilter,
        "rating",
        "user__is_host",
        "room__category",
        "room__pet_friendly",
    )
