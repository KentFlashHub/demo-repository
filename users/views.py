from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.shortcuts import redirect
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import redirect
from allauth.exceptions import ImmediateHttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout
from flashcards.views import get_base_context

from files.models import Directory

class CustomGoogleOAuth2Adapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):

        if not User.objects.filter(email=sociallogin.account.extra_data['email']):
            user = sociallogin.user
            user.set_unusable_password()
            user.username = user.email.split('@')[0]
            user.first_name = sociallogin.account.extra_data['given_name']
            user.save()
            
            # create a directory for the user
            Directory.objects.create(user=user, name=user.username, parent_directory=None)

        else:
            sociallogin.user = User.objects.get(email=sociallogin.account.extra_data['email'])

        user_email = sociallogin.account.extra_data['email']#TODO: interrupt signup if email is not a kent email
        if not user_email.endswith('@kent.edu'):
            return ImmediateHttpResponse("users/login.html?error=invalid_email")

    
def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You are able to login!')
            return redirect('login')
    else:
        form = UserRegisterForm()

    context = get_base_context(request)
    context['form'] = form

    return render(request, 'users/register.html', context)

def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    context = get_base_context(request)
    return render(request, 'users/login.html', context)

def logout_view(request):
    if not request.user.is_authenticated:
        return redirect('home')
    context = get_base_context(request)
    logout(request)
    return render(request, 'users/logout.html', context)

