

# Create your views here.
import requests
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render
from django.db.models import Avg
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import MovieReview
from django.views.decorators.csrf import csrf_exempt
from .models import MovieReview, ReviewVote
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout


TMDB_API_KEY = "5c479c251bf591218affcb56eea2816d"

def search_movie(request):
    query = request.GET.get("query", "")
    if not query:
        return JsonResponse({"error": "No search query provided"}, status=400)

    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}"
    response = requests.get(url)

    if response.status_code == 200:
        return JsonResponse(response.json(), safe=False)
    else:
        return JsonResponse({"error": "Movie not found"}, status=404)


def search_page(request):
    return render(request, "search.html")

@login_required
def movie_detail(request, movie_id):
    # Fetch movie details from TMDb API
    movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
    movie_response = requests.get(movie_url)

    if movie_response.status_code != 200:
        return render(request, "404.html", {"error": "Movie not found"})

    movie_data = movie_response.json()

    # Handle Review Submission (POST Request)
    if request.method == "POST":
        rating = request.POST.get("rating")
        review_text = request.POST.get("review_text")

        # Save the user's review
        MovieReview.objects.create(
            movie_id=movie_id,
            user=request.user,
            rating=rating,
            review_text=review_text
        )

        # Redirect to the same page after submission
        return HttpResponseRedirect(request.path)

    # Fetch all reviews and calculate average rating
    reviews = MovieReview.objects.filter(movie_id=movie_id)
    avg_rating = reviews.aggregate(Avg("rating"))["rating__avg"]
    avg_rating = round(avg_rating, 1) if avg_rating else "No ratings yet"

    context = {
        "movie": movie_data,
        "reviews": reviews,
        "avg_rating": avg_rating,
    }

    return render(request, "movie_detail.html", context)

@csrf_exempt
@csrf_exempt
def vote_review(request, review_id, vote_type):
    if vote_type not in ['like', 'dislike']:
        return JsonResponse({"error": "Invalid vote type"}, status=400)

    try:
        review = MovieReview.objects.get(id=review_id)
        user = request.user

        # Check if the user has already voted
        existing_vote = ReviewVote.objects.filter(user=user, review=review).first()

        if existing_vote:
            # If the same vote is repeated, ignore it
            if existing_vote.vote_type == vote_type:
                return JsonResponse({"message": "You have already voted", "likes": review.likes, "dislikes": review.dislikes})

            # If the vote type changes, update counts
            if existing_vote.vote_type == 'like':
                review.likes -= 1
            else:
                review.dislikes -= 1

            # Update to new vote
            existing_vote.vote_type = vote_type
            existing_vote.save()

        else:
            # If no vote exists, create a new one
            ReviewVote.objects.create(user=user, review=review, vote_type=vote_type)

        # Update the like/dislike count
        if vote_type == 'like':
            review.likes += 1
        else:
            review.dislikes += 1

        review.save()

        return JsonResponse({"likes": review.likes, "dislikes": review.dislikes})

    except MovieReview.DoesNotExist:
        return JsonResponse({"error": "Review not found"}, status=404)
    
def home_page(request):
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    movies = response.json().get("results", []) if response.status_code == 200 else []
    return render(request, "home.html", {"movies": movies})

def about(request):
    return render(request, 'about.html')  # Render the about page template


def login_page(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home_page")  # Redirect to the homepage
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")


def signup_page(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        # Check if passwords match
        if password != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, "signup.html")

        # Check if username is taken
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return render(request, "signup.html")

        # Check if email is already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, "signup.html")

        # Create and login the user
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect("home_page")  # Redirect to homepage

    return render(request, "signup.html")

def logout_user(request):
    logout(request)
    return redirect('login')  # Redirect to the homepage or login page after logout


@login_required
def profile_page(request):
    return render(request, 'profile.html', {'user': request.user})