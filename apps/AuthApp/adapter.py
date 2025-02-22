from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_email
from django.contrib.auth import get_user_model


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        email = user_email(sociallogin.user)

        # Check if a user with the given email already exists
        existing_user = get_user_model().objects.filter(email=email).first()

        if existing_user:
            # Connect the social account to the existing user
            sociallogin.connect(request, existing_user)
            return existing_user
        else:
            u = sociallogin.user
            u.set_unusable_password()
            if form:
                self.get_account_adapter().save_user(request, u, form)
            else:
                self.get_account_adapter().populate_username(request, u)
            sociallogin.save(request)
            return u
