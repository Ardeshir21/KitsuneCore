# context_processors.py
from Apps.UserAuthentication.context_data import AuthenticationForms_context
# from .context_data_2 import generate_custom_data_2


def all_custom_context(request):
    # Simply call the functions from other context files to get the dynamically generated context data
    auth_forms = AuthenticationForms_context(request)
    data_2 = {'dummy': 'dummy_context'}

    # Merge the context data from different sources
    custom_data = {**auth_forms, **data_2}

    return custom_data
