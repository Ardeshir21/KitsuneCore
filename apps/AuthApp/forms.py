from django import forms
from allauth.account.forms import ResetPasswordForm
from django.utils.translation import gettext_lazy as _


# This is inherited form ResetPasswordForm from AllAuth app which is ModelForm itself.
# There is no need to write any views.py for this form. It uses the AllAuth views.
class CustomResetPasswordForm(ResetPasswordForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        # A widget for email field
        email_widget = forms.TextInput(
            attrs={
                "type": "email",
                "placeholder": _("E-mail address"),
                "autocomplete": "email",
                "class": "form-control",
            }
        )

        self.fields["email"] = forms.EmailField(label=_("E-mail"), widget=email_widget)
