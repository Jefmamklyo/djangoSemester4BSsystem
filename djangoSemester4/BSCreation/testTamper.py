# test_tamper.py
from BSCreation.models import User, UserAccount
from merkleTree.models import Transaction
from merkleTree.service import MerkleTreeService

user1 = User.objects.get(username="testAccount1")
account1 = UserAccount.objects.get(user=user1)
tx = Transaction.objects.filter(account=account1).order_by("createdAt").first()

service = MerkleTreeService()
print("Before tamper:", service.merkleProof(tx.id))

Transaction.objects.filter(id=tx.id).update(jsonData={"sender": "tampered", "receiver": "tampered", "amount": "999999.00"})

print("After tamper:", service.merkleProof(tx.id))