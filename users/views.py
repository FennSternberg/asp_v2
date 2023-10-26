from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import LoginForm, RegistrationForm
from .models import UserProfile
from django.contrib.auth.models import User

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        
        # Check if a user with the provided username exists
        try:
            user = User.objects.get(username=request.POST['username'])
        except User.DoesNotExist:
            user = None
        
        # If the user exists, check their credentials
        if user:
            # Validate password
            if user.check_password(request.POST['password']):
                # Check if the user is active
                if user.is_active:
                    login(request, user)
                    return redirect('homepage')
                else:
                    # Redirect to the "awaiting authentication" page if the user is inactive
                    return redirect('account_awaiting_authentication')
            else:
                # Invalid password
                form.add_error(None, 'Invalid username or password')
        else:
            # Invalid username
            form.add_error(None, 'Invalid username or password')
            
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Use set_password to hash the password
            user.is_active = False
            user.save()

            # Handle UserProfile creation
            profile = UserProfile(user=user, usergroup='regular', location=form.cleaned_data['location'])
            profile.save()

            login(request, user)  # Log the user in
            return redirect('account_awaiting_authentication') 
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def account_awaiting_authentication(request):
    return render(request, 'account_awaiting_authentication.html')

from django.shortcuts import render, redirect
from .forms import UpdateUserForm, UpdateUserProfileForm

def update_profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateUserProfileForm(request.POST, instance=request.user.userprofile)  # Assuming profile as the related_name in UserProfile model
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return render(request, 'update_profile.html', {
                    'user_form': user_form,
                    'profile_form': profile_form,
                })
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateUserProfileForm(instance=request.user.userprofile)

    return render(request, 'update_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })
