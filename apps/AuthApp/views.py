from django.shortcuts import render
from django.views import generic
from allauth.account.views import (
    LoginView,
    SignupView,
    ConfirmEmailView,
    EmailView,
    EmailVerificationSentView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetFromKeyView,
    PasswordResetFromKeyDoneView,
    PasswordChangeView,
    AccountInactiveView,
    ReauthenticateView,
    PasswordSetView,
)

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.conf import settings
from django.http import HttpResponseRedirect


# The views are inherited from allAuth to override them if needed.
# In addition, with using the same url pattern Names as allAuth, you can use your own url path for the authentication app


# Login View
class CustomLoginView(LoginView):
    """
    This view is inherited from allAuth LoginView to override the template and messages
    """
    template_name = 'AuthApp/login.html'
    
    def form_invalid(self, form):
        # Add an error message for invalid form data
        messages.error(
            self.request,
            "Invalid email or password. Please correct the errors and try again.",
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Login'
        context['PAGE_META'] = {
            'PAGE_TITLE': 'Login | ' + settings.APP_INFO['APP_NAME'],
            'META_DESCRIPTION': 'Securely login to your account to access your dashboard and personal settings.',
            'META_KEYWORDS': 'login, sign in, account access, secure login, ' + settings.APP_INFO['APP_NAME'].lower(),
            'CANONICAL_URL': f"{settings.SITE_URL}{reverse('account_login')}",
            'ROBOTS_CONTENT': 'noindex, nofollow',
            'OG_IMAGE_1080x1080_PATH': '',
        }
        return context


# Signup View
class CustomRegisterView(SignupView):
    template_name = 'AuthApp/signup.html'

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Please correct the errors below.",
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Sign Up'
        context['PAGE_META'] = {
            'PAGE_TITLE': 'Create Account | ' + settings.APP_INFO['APP_NAME'],
            'META_DESCRIPTION': 'Create a new account to access our services and features. Join ' + settings.APP_INFO['APP_NAME'] + ' today.',
            'META_KEYWORDS': 'sign up, register, create account, new user, ' + settings.APP_INFO['APP_NAME'].lower(),
            'CANONICAL_URL': f"{settings.SITE_URL}{reverse('account_signup')}",
            'ROBOTS_CONTENT': 'noindex, nofollow',
            'OG_IMAGE_1080x1080_PATH': '',
        }
        return context




# Email Verification View
class CustomEmailVerificationSentView(EmailVerificationSentView):
    template_name = 'AuthApp/verification_sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Verification Email Sent'
        context['PAGE_META'] = {
            'PAGE_TITLE': 'Email Verification Sent | ' + settings.APP_INFO['APP_NAME'],
            'META_DESCRIPTION': 'Please check your email to verify your account.',
            'META_KEYWORDS': 'email verification, account verification, confirm email',
            'CANONICAL_URL': f"{settings.SITE_URL}{reverse('account_email_verification_sent')}",
            'ROBOTS_CONTENT': 'noindex, nofollow',
            'OG_IMAGE_1080x1080_PATH': settings.APP_INFO['PAGE_META_INFO']['OG_IMAGE_1080x1080_PATH'],
        }
        return context


# Confirm Email View
class CustomConfirmEmailView(ConfirmEmailView):
    template_name = 'AuthApp/email_confirm.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Confirm Email'
        context['PAGE_META'] = {
            'PAGE_TITLE': 'Confirm Email | ' + settings.APP_INFO['APP_NAME'],
            'META_DESCRIPTION': 'Confirm your email address to complete your registration.',
            'META_KEYWORDS': 'confirm email, email verification, verify account',
            'CANONICAL_URL': f"{settings.SITE_URL}{reverse('account_confirm_email', args=['dummy'])}",
            'ROBOTS_CONTENT': 'noindex, nofollow',
            'OG_IMAGE_1080x1080_PATH': '',
        }
        return context


# Logout View
class CustomLogoutView(LogoutView):
    template_name = 'AuthApp/logout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Sign Out'
        context['PAGE_META'] = {
            'PAGE_TITLE': 'Sign Out | ' + settings.APP_INFO['APP_NAME'],
            'META_DESCRIPTION': 'Securely sign out from your account.',
            'META_KEYWORDS': 'logout, sign out, exit account',
            'CANONICAL_URL': f"{settings.SITE_URL}{reverse('account_logout')}",
            'ROBOTS_CONTENT': 'noindex, nofollow',
            'OG_IMAGE_1080x1080_PATH': '',
        }
        return context


# Password Reset View
class CustomPasswordResetView(PasswordResetView):
    template_name = 'AuthApp/password_reset.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Reset Password'
        context['PAGE_META'] = {
            'PAGE_TITLE': 'Reset Your Password',
            'META_DESCRIPTION': 'Reset your account password securely.',
            'META_KEYWORDS': 'password reset, forgot password, account recovery',
            'CANONICAL_URL': f"{settings.SITE_URL}{reverse('account_reset_password')}",
            'ROBOTS_CONTENT': 'noindex, nofollow',
        }
        return context


# Password Reset Done View
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'AuthApp/password_reset_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Password Reset Email Sent'
        context['PAGE_META'] = {
            'PAGE_TITLE': 'Password Reset Email Sent | ' + settings.APP_INFO['APP_NAME'],
            'META_DESCRIPTION': 'Password reset instructions have been sent to your email.',
            'META_KEYWORDS': 'password reset, reset confirmation, account recovery',
            'CANONICAL_URL': f"{settings.SITE_URL}{reverse('account_reset_password_done')}",
            'ROBOTS_CONTENT': 'noindex, nofollow',
            'OG_IMAGE_1080x1080_PATH': '',
        }
        return context


# Password Reset From Key View
class CustomPasswordResetFromKeyView(PasswordResetFromKeyView):
    template_name = 'AuthApp/password_reset_from_key.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Set New Password'
        context['PAGE_META'] = {
            'PAGE_TITLE': 'Set New Password | ' + settings.APP_INFO['APP_NAME'],
            'META_DESCRIPTION': 'Create a new password for your account.',
            'META_KEYWORDS': 'new password, reset password, password recovery',
            'CANONICAL_URL': f"{settings.SITE_URL}{reverse('account_reset_password_from_key', args=['dummy', 'dummy'])}",
            'ROBOTS_CONTENT': 'noindex, nofollow',
            'OG_IMAGE_1080x1080_PATH': '',
        }
        return context


# Password Reset From Key Done View
class CustomPasswordResetFromKeyDoneView(PasswordResetFromKeyDoneView):
    template_name = 'AuthApp/password_reset_from_key_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Password Reset Complete'
        context['PAGE_META'] = {
            'PAGE_TITLE': 'Password Reset Complete | ' + settings.APP_INFO['APP_NAME'],
            'META_DESCRIPTION': 'Your password has been successfully reset.',
            'META_KEYWORDS': 'password reset complete, reset successful, account recovery',
            'CANONICAL_URL': f"{settings.SITE_URL}{reverse('account_reset_password_from_key_done')}",
            'ROBOTS_CONTENT': 'noindex, nofollow',
            'OG_IMAGE_1080x1080_PATH': '',
        }
        return context


# Password Change View
class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'AuthApp/password_change.html'
    success_url = reverse_lazy('account_login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Change Password'
        context['PAGE_META'] = {
            'PAGE_TITLE': 'Change Password | ' + settings.APP_INFO['APP_NAME'],
            'META_DESCRIPTION': 'Securely change your account password.',
            'META_KEYWORDS': 'change password, update password, account security',
            'CANONICAL_URL': f"{settings.SITE_URL}{reverse('account_change_password')}",
            'ROBOTS_CONTENT': 'noindex, nofollow',
            'OG_IMAGE_1080x1080_PATH': '',
        }
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            "Please login with your new password.",
        )
        # Log the user out
        logout(self.request)
        return response

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Please correct the errors below.",
        )
        return super().form_invalid(form)


# Account Inactive View
class CustomAccountInactiveView(AccountInactiveView):
    template_name = 'AuthApp/account_inactive.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Account Inactive'
        context['PAGE_META'] = {
            'PAGE_TITLE': 'Account Inactive | ' + settings.APP_INFO['APP_NAME'],
            'META_DESCRIPTION': 'Your account is currently inactive. Please contact support for assistance.',
            'META_KEYWORDS': 'inactive account, account status, account suspended',
            'CANONICAL_URL': f"{settings.SITE_URL}{reverse('account_inactive')}",
            'ROBOTS_CONTENT': 'noindex, nofollow',
            'OG_IMAGE_1080x1080_PATH': '',
        }
        return context


# Reauthenticate View
class CustomReauthenticateView(ReauthenticateView):
    template_name = 'AuthApp/reauthenticate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Reauthenticate'
        context['PAGE_META'] = {
            'PAGE_TITLE': 'Reauthenticate | ' + settings.APP_INFO['APP_NAME'],
            'META_DESCRIPTION': 'Please reauthenticate to confirm your identity.',
            'META_KEYWORDS': 'reauthenticate, verify identity, security check',
            'CANONICAL_URL': f"{settings.SITE_URL}{reverse('account_reauthenticate')}",
            'ROBOTS_CONTENT': 'noindex, nofollow',
            'OG_IMAGE_1080x1080_PATH': '',
        }
        return context


# Email Management View
class CustomEmailView(LoginRequiredMixin, EmailView):
    template_name = 'AuthApp/email.html'

    def dispatch(self, request, *args, **kwargs):
        # If ACCOUNT_MAX_EMAIL_ADDRESSES is 1, redirect to home
        if getattr(settings, 'ACCOUNT_MAX_EMAIL_ADDRESSES', 1) == 1:
            return HttpResponseRedirect(reverse('home'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Email Management'
        context['PAGE_META'] = {
            'PAGE_TITLE': 'Email Management | ' + settings.APP_INFO['APP_NAME'],
            'META_DESCRIPTION': 'Manage your account email addresses and preferences.',
            'META_KEYWORDS': 'email management, account settings, email preferences',
            'CANONICAL_URL': f"{settings.SITE_URL}{reverse('account_email')}",
            'ROBOTS_CONTENT': 'noindex, nofollow',
            'OG_IMAGE_1080x1080_PATH': '',
        }
        return context


# Password Set View (for social accounts)
class CustomPasswordSetView(LoginRequiredMixin, PasswordSetView):
    template_name = 'AuthApp/password_set.html'
    success_url = reverse_lazy('account_login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Set Password'
        context['PAGE_META'] = {
            'PAGE_TITLE': 'Set Password | ' + settings.APP_INFO['APP_NAME'],
            'META_DESCRIPTION': 'Set a password for your social account.',
            'META_KEYWORDS': 'set password, create password, social account',
            'CANONICAL_URL': f"{settings.SITE_URL}{reverse('account_set_password')}",
            'ROBOTS_CONTENT': 'noindex, nofollow',
            'OG_IMAGE_1080x1080_PATH': '',
        }
        return context
