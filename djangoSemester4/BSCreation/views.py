from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import signupForm
from .models import User

# Create your views here.
class signUpView(CreateView):
    model = User
    form_class = signupForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        User.objects.create(user=self.object)
        return response