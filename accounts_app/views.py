from accounts_app.forms import RegistrationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView


class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = "accounts_app/registration.html"
    success_url = reverse_lazy("login")
