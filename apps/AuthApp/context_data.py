# context_processors.py
from allauth.account.forms import LoginForm, SignupForm, ResetPasswordForm
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm


def AuthenticationForms_context(request):

    all_forms = {'login_form': LoginForm
    }

    return all_forms