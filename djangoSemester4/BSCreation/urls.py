#app level url.py 


from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from django.urls import path
from .views import signUpView, IndexView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("signup/", signUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(template_name="BSCreation/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
]