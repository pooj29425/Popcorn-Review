from django.shortcuts import render, redirect
from .forms import UserProfileForm, UserForm
from .models import UserProfile
from django.contrib.auth.decorators import login_required

@login_required
def edit_profile(request):
    user = request.user  # Get logged-in user

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')  # Redirect to profile page after saving
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=user.userprofile)

    return render(request, 'edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})