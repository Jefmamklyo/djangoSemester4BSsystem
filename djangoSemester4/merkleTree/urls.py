########## MERKLE TREE APP LEVEL  URLS.PY ##########
from django.urls import path
from .views import transferView, transactionList, merkleStatus

urlpatterns = [
    path("transfer/", transferView, name="transfer"),
    path("transactions/", transactionList, name="transactionList"),
    path("chain-status/", merkleStatus, name="merkleStatus"),
]