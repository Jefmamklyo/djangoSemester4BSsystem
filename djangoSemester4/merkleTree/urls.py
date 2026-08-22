########## MERKLE TREE APP LEVEL  URLS.PY ##########
from django.urls import path
from .views import transferView, transactionList, merkleStatus

urlpatterns = [
    path("transfer/", transferView, name="transfer"),
    path("transactions/", transactionList, name="transaction_list"),
    path("chain-status/", merkleStatus, name="chain_status"),
]