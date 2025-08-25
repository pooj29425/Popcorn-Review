"""
URL configuration for popcorn_review project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from reviews.views import search_movie, search_page, movie_detail, vote_review, home_page, about
from reviews.views import login_page
from reviews.views import signup_page
from reviews.views import logout_user
from django.contrib.auth import views as auth_views
from reviews.views import profile_page
from users import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/search/', search_movie, name='search_movie'),
    path('search/', search_page, name='search_page'),
    path('movie/<int:movie_id>/', movie_detail, name='movie_detail'),  # New route for movie details
    path('api/vote/<int:review_id>/<str:vote_type>/', vote_review, name='vote_review'),
    path('', home_page, name='home_page'),  # for the homepage
    path('about/', about, name='about'),  # for the About page
    path("login/", login_page, name="login"),
    path("signup/", signup_page, name="signup"),
    path('logout/', logout_user, name='logout'),
    path('profile/', profile_page, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    
    
     # Password Reset URLs
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
