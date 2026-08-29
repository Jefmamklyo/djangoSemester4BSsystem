from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from BSCreation.models import UserAccount
from .models import Transaction
from .forms import TransferForm
from .service import MerkleTreeService
from django.db import transaction 

from BSCreation.crypt import hashLookups



@login_required
def transferView(request):
    sender = get_object_or_404(UserAccount, user=request.user)# get sender object

    if request.method == "POST":
        form = TransferForm(request.POST) #validate form
        if form.is_valid():
            receiverLookup = hashLookups(form.cleaned_data["reciever"]) #gegt id but in hashed form through conversion
 
            amount = form.cleaned_data["amount"]#gather post data


            receiver = UserAccount.objects.filter(accountLookup=receiverLookup).first() #get reciveer id and chekck if they existst
            #valdiation methods so transfer itself is valid
            if receiver is None:
                form.add_error("reciever", "That account does not exist.")
            elif receiver.id == sender.id:
                form.add_error("reciever", "You cannot transfer to your own account.")
            elif sender.balance < amount:
                form.add_error("amount", "Insufficient funds.")
            else:
                with transaction.atomic():
                    #transfer logic
                    sender.balance -= amount
                    receiver.balance += amount
                    sender.save()
                    receiver.save()

                    #send data to jsonData for merkle tree
                    seralisedData = {
                        "sender": sender.accountLookup,
                        "receiver": receiver.accountLookup,
                        "amount": str(amount),
                    }
                    Transaction.objects.create(account=sender, jsonData=seralisedData)

                return redirect("transactionList")
    else:
        form = TransferForm()

    return render(request, "merkleTree/transfer.html", {"form": form, "balance": sender.balance, "id": sender.getAccountNumber()})


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


    
    latest = transactions.first()
    root_hash = latest.merkleRootHash if latest else None


    return render(request, "merkleTree/merkleStatus.html", {"results": results, "root_hash": root_hash,})