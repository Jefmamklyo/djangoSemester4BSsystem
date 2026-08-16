from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import signupForm
from .models import User, UserAccount

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "BSCreation/index.html"
    login_url = "login"

class signUpView(CreateView):
    model = User
    form_class = signupForm
    template_name = 'BSCreation/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        UserAccount.objects.create(user=self.object)
        return response