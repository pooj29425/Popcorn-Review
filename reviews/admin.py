# Register your models here.

from django.contrib import admin
from .models import MovieReview

@admin.register(MovieReview)
class MovieReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie_id', 'rating', 'created_at')  # Columns shown in the admin panel
    search_fields = ('movie_id', 'user__username')  # Search by movie ID or username
    list_filter = ('rating', 'created_at')  # Filters for better navigation

