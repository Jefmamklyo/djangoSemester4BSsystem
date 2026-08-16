from django.contrib.auth.forms import UserCreationForm
from .models import User

class signupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username']