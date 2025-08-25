# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class MovieReview(models.Model):
    movie_id = models.CharField(max_length=100)  # Stores movie ID from external API (e.g., TMDb)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links to the reviewer
    review_text = models.TextField()  # Stores the review content
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating from 1 to 5
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the review was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for last update
    # New fields for likes and dislikes
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    def __str__(self):
        return f"Review by {self.user.username} for Movie {self.movie_id}"

class ReviewVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(MovieReview, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=10, choices=[('like', 'Like'), ('dislike', 'Dislike')])

    class Meta:
        unique_together = ('user', 'review')  # Ensure one vote per user per review