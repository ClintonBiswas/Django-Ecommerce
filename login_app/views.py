from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages

#authentication
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

#Forms And models
from login_app.models import User, Profile
from login_app.forms import ProfileForm, SignupForm

# Create your views here.
def Sign_UP(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!!')
            return HttpResponseRedirect(reverse('login_app:login'))
    diction = {'signup_form': form}
    return render(request, 'login_app/sign_up.html', context=diction)

def user_login(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username = username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('shop_app:home'))
    diction = {'login_form': form}
    return render(request, 'login_app/login.html', context=diction)

@login_required
def logout_user(request):
    logout(request)
    messages.success(request, 'You are logged Out')
    return HttpResponseRedirect(reverse('shop_app:home'))

@login_required
def user_profile(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST,instance=profile)
        if form.is_valid():
            form.save()
            form = ProfileForm(instance=profile)
            messages.info(request, 'Profile updated successfully!!')
            #return HttpResponse('Successfully')
    diction = {'profile_form': form}
    return render(request, 'login_app/profile.html', context = diction)
