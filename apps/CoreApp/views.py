from django.shortcuts import render
from django.views import generic
from django.core.mail import send_mail
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect



class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            # User is logged in but not an admin
            messages.error(self.request, "You do not have permission to access this page.")
            return redirect("HomeApp:home")  # Redirect to home page
        else:
            # User is not logged in
            messages.error(self.request, "Please log in to continue.")
            return redirect("account_login")