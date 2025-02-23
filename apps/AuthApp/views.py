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
        return context




# Email Verification View
class CustomEmailVerificationSentView(EmailVerificationSentView):
    template_name = 'AuthApp/verification_sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Verification Email Sent'
        return context


# Confirm Email View
class CustomConfirmEmailView(ConfirmEmailView):
    template_name = 'AuthApp/email_confirm.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Confirm Email'
        return context


# Logout View
class CustomLogoutView(LogoutView):
    template_name = 'AuthApp/logout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Sign Out'
        return context


# Password Reset View
class CustomPasswordResetView(PasswordResetView):
    template_name = 'AuthApp/password_reset.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Reset Password'
        return context


# Password Reset Done View
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'AuthApp/password_reset_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Password Reset Email Sent'
        return context


# Password Reset From Key View
class CustomPasswordResetFromKeyView(PasswordResetFromKeyView):
    template_name = 'AuthApp/password_reset_from_key.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Set New Password'
        return context


# Password Reset From Key Done View
class CustomPasswordResetFromKeyDoneView(PasswordResetFromKeyDoneView):
    template_name = 'AuthApp/password_reset_from_key_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Password Reset Complete'
        return context


# Password Change View
class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'AuthApp/password_change.html'
    success_url = reverse_lazy('account_login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Change Password'
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
        return context


# Reauthenticate View
class CustomReauthenticateView(ReauthenticateView):
    template_name = 'AuthApp/reauthenticate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Reauthenticate'
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
        return context


# Password Set View (for social accounts)
class CustomPasswordSetView(LoginRequiredMixin, PasswordSetView):
    template_name = 'AuthApp/password_set.html'
    success_url = reverse_lazy('account_login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Set Password'
        return context
