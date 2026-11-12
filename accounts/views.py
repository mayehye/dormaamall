
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import UserUpdateForm, ProfileUpdateForm
from .models import UserProfile


def register_view(request):
    if request.user.is_authenticated:
        return redirect('listings:home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            # Create user profile if it doesn't exist
            UserProfile.objects.get_or_create(user=user)

            messages.success(
                request,
                f"Welcome to Dormaa Mall, {user.username}!"
            )
            return redirect('listings:home')

    else:
        form = UserCreationForm()

    return render(request, 'accounts/register.html', {
        'form': form
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('listings:home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Ensure user profile exists
            UserProfile.objects.get_or_create(user=user)

            messages.success(
                request,
                f"Welcome back, {user.username}!"
            )

            next_url = request.POST.get('next') or request.GET.get('next')

            return redirect(next_url if next_url else 'listings:home')

    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {
        'form': form
    })


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('listings:home')


@login_required
def profile_edit_view(request):
    # Get or create the user's profile
    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':
        u_form = UserUpdateForm(
            request.POST,
            instance=request.user
        )

        p_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            messages.success(
                request,
                'Your profile and profile picture have been updated successfully!'
            )

            return redirect('accounts:profile_edit')

        messages.error(
            request,
            'Please correct the errors below.'
        )

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(
        request,
        'accounts/profile_edit.html',
        context
    )
