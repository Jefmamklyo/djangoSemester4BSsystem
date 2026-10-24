from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import signupForm
from .models import User, UserAccount

import json
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from .forms import cardTokenForm
from .models import UserAccount


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




@login_required
def addCard__(request):
    account = get_object_or_404(UserAccount, user=request.user)
    return render(request, "BSCreation/addCard.html", {
        "stripe_publishable_key": settings.STRIPE_PUBLISHABLE_KEY,
        "hasCard": bool(account.encryptedPaymentMethod),
    })


@login_required
@require_POST
def saveCard(request):
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if isinstance(payload, dict):
        form = cardTokenForm(payload)
    else:
        form = {} #empty value

    
    if not form.is_valid():
        return JsonResponse({"error": "INVALID PAYMENT METHOD"}, status=400)

    account = get_object_or_404(UserAccount, user=request.user)  #Non client request
    #Encrypt payment method id
    account.encryptToken(form.cleaned_data["paymentMethodId"])

    account.save(update_fields=["encryptedPaymentMethod"])
    return JsonResponse({"success": True})