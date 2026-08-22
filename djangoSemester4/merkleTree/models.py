from django.db import models
from BSCreation.models import UserAccount

class Transaction(models.Model):
    account = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    merkleLeafHash = models.CharField(max_length=64)
    merkleRootHash = models.CharField(max_length=64)
    jsonData = models.JSONField()

    def __str__(self):
        return super().__str__()