from accounts_app.views import RegistrationView
from django.contrib.auth.views import LoginView
from django.urls import path

urlpatterns = [
    path("registration/", RegistrationView.as_view(), name="registration"),
    path(
        "login/",
        LoginView.as_view(template_name="accounts_app/login.html"),
        name="login"
    )
]
