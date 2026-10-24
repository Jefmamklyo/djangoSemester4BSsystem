from django.contrib.auth.forms import UserCreationForm
from .models import User

from django import forms

class signupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username']


#pete integration, regex pattern for card number validation
#String pattern validates payment id methods
#pm: PaymentMethod prefix

class cardTokenForm(forms.Form):
    paymentMethodId = forms.RegexField(regex=r"^pm_[A-Za-z0-9_]{8,64}$", max_length=100)