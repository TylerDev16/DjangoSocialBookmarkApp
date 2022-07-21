from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile

# Create your views here.


def user_login(request):
    if request.method == "POST":
        # instantiate the form with submitted data
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # authenticate user against db
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            # checks if user exists
            if user is not None:
                # if user exists and is active, login successful
                if user.is_active:
                    # if user is active and authenticated, set user to current session
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                # if user exists but is not active, account is disabled
                else:
                    return HttpResponse('Disabled Account')
            # user is not authenticated
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # create profile for new user
            Profile.objects.create(user=new_user)
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': dashboard})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
        else:
            messages.error(request, 'Error updating you profile.')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form })