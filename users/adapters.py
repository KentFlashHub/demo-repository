from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.http import HttpResponseRedirect

class CustomGoogleOAuth2Adapter(GoogleOAuth2Adapter):
    def sociallogin_from_response(self, request, response):
        social_login = super().sociallogin_from_response(request, response)
        email = social_login.account.extra_data.get('email')
        
        if email and not email.endswith('@kent.edu'):
            # Redirect to an error page or display an error message
            print("Definitely an invalid email!!!!!!!!!!!!!!")
            return HttpResponseRedirect('/account/login/?error=invalid_email')
        
        return social_login

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        email = sociallogin.account.extra_data.get('email')
        
        if email and email.endswith('@kent.edu'):
            return True
        
        return False