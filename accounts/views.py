from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from .models import Notification
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm
from bookings.models import Booking

def register_view(request):
    """
    Registers a new user and logs them in immediately.
    """
    if request.user.is_authenticated:
        return redirect('event_list')

    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to the Event Portal, {user.first_name}!")
            return redirect('event_list')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """
    Authenticates and logs in users, with clean messaging.
    """
    if request.user.is_authenticated:
        return redirect('event_list')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name}!")
            # Handle redirect to next page if available
            next_url = request.GET.get('next', 'event_list')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'accounts/login.html')


def logout_view(request):
    """
    Logs out the user and displays a farewell message.
    """
    logout(request)
    messages.info(request, "You have logged out successfully.")
    return redirect('event_list')


@login_required
def profile_view(request):
    """
    Displays the user's booking history and handles profile detail updates.
    """
    user_bookings = Booking.objects.filter(user=request.user).order_by('-created_at')

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors in the profile form.")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    notifications = Notification.objects.filter(is_active=True).order_by('-created_at')[:5]

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'bookings': user_bookings,
        'notifications': notifications,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def delete_account_view(request):
    """
    Deletes the currently logged-in user account after password confirmation.
    """
    if request.method == 'POST':
        password = request.POST.get('password')
        user = request.user
        if user.check_password(password):
            logout(request)
            user.delete()
            messages.success(request, 'Your account has been deleted successfully.')
            return redirect('event_list')

        messages.error(request, 'The password you entered is incorrect.')
        return redirect('profile')

    return redirect('profile')


@login_required
def change_password_view(request):
    """
    Handles user password changes securely.
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in
            messages.success(request, "Your password was successfully updated!")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors in the password change form.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})
