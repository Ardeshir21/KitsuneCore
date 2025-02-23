from django.urls import reverse_lazy


# allAuth Settings
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

AUTH_USER_MODEL = 'AuthApp.CoreUser'

LOGIN_REDIRECT_URL = reverse_lazy('home')
LOGIN_URL = reverse_lazy('account_login')

# ACCOUNT_ADAPTER = 'apps.AuthApp.adaptor.AccountAdapter'

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE  = False
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_MAX_EMAIL_ADDRESSES = 1
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_SIGNUP_REDIRECT_URL = reverse_lazy('account_login')
EMAIL_RESEND_COOLDOWN_MINUTES = 5 
EMAIL_RESEND_LIMIT = 8

SOCIALACCOUNT_LOGIN_ON_GET = True # It goes directly to 3rd-party authentication page. The "SOCIALACCOUNT_" is the prefix for app_settings of SocialApp
# SOCIALACCOUNT_ADAPTER = 'Apps.UserAuthentication.adapter.MySocialAccountAdapter'

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'offline',
        },
        'OAUTH_PKCE_ENABLED': True,
    }
}

# Session Settings
SESSION_COOKIE_AGE = 1209600  # 2 weeks in seconds
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
ACCOUNT_SESSION_REMEMBER = None  # None means ask the user, True/False is forced
