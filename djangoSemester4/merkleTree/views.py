import stat

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from BSCreation.models import UserAccount
from .models import Transaction
from .forms import TransferForm
from .service import verify_transaction



# Create your views here.
@login_required
def transferView(request):
    if request.method == "POST":
        form = TransferForm(request.POST)
        if form.is_valid():
            sender = UserAccount.objects.get(user=request.user)    
            seralisedData = { 
                "sender": sender.id,
                "receiver": form.cleaned_data["receiver"].id,
                "amount": form.cleaned_data["amount"],
                }
            Transaction.objects.create(accounts = sender, jsonData=seralisedData)
            return redirect("transaction_list")
        else:
            form = TransferForm()
    return render(request, "merkleTree/index.html", {"form": form})


@login_required
def transactionList(request):
    transactions = Transaction.objects.filter(account__user=request.user).order_by("-createdAt")
    return render(request, "merkleTree/transactionList.html", {"transactions": transactions})


@login_required
def merkleStatus(request):
    transactions = Transaction.objects.filter(account__user=request.user).order_by("-createdAt")
    results = []
    for tx in transactions:
        status = verify_transaction(tx.id)
        results.append((tx,status))
    return render(request, "ledger/chainStatus.html", {"results": results})
