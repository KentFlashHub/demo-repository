import random
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.shortcuts import redirect
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from django.http import HttpResponseRedirect
from Django_Flashcards.settings import CLIENT_ID

from django.shortcuts import redirect
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.exceptions import ImmediateHttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

class CustomGoogleOAuth2Adapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):

        if not User.objects.filter(email=sociallogin.account.extra_data['email']):
            user = sociallogin.user
            user.set_unusable_password()
            user.username = user.email.split('@')[0]
            user.first_name = sociallogin.account.extra_data['given_name']
            user.save()
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
    return render(request, 'users/register.html', {'form': form})