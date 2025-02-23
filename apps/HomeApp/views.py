from django.shortcuts import render
from django.views import generic



class HomeView(generic.TemplateView):
    template_name = 'HomeApp/molla/index.html'

    def dispatch(self, request, *args, **kwargs):
        # Any Test Code Here
        # Specific Use Cases:
        # Pre-rendering Data Preparation: Fetching or manipulating data required for the template before rendering.
        # Access Control: Implementing authentication or authorization checks to restrict access to certain users.
        # Dynamic Template Selection: Choosing the appropriate template based on conditions or user input.
        # Custom Rendering Logic: Handling special cases or alternative rendering approaches.


        # Call the parent class's dispatch method to continue processing the request
        return super().dispatch(request, *args, **kwargs)