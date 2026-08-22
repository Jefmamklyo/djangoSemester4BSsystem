from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from BSCreation.models import UserAccount
from .models import Transaction
from .forms import TransferForm
from .service import MerkleTreeService



@login_required
def transferView(request):
    if request.method == "POST":
        form = TransferForm(request.POST)
        if form.is_valid():
            sender = UserAccount.objects.get(user=request.user)
            seralisedData = {
                "sender": sender.id,
                "receiver": form.cleaned_data["reciever"],
                "amount": str(form.cleaned_data["amount"]),  # Decimal -> str, JSON-safe
            }
            Transaction.objects.create(account=sender, jsonData=seralisedData)
            return redirect("transactionList")
    else:
        form = TransferForm()
    return render(request, "merkleTree/transfer.html", {"form": form})


@login_required
def transactionList(request):
    transactions = Transaction.objects.filter(account__user=request.user).order_by("-createdAt")
    return render(request, "merkleTree/trasactionList.html", {"transactions": transactions})


@login_required
def merkleStatus(request):
    transactions = Transaction.objects.filter(account__user=request.user).order_by("-createdAt")
    results = []
    for tx in transactions:
        status = MerkleTreeService().merkleProof(tx.id)
        results.append((tx,status))
    return render(request, "merkleTree/merkleStatus.html", {"results": results})