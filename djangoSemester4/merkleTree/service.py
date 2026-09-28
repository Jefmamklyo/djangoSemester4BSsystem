import json
from .models import Transaction
from pymerkle import InmemoryTree, verify_inclusion
from django.db import transaction as db_transaction
from pymerkle.hasher import MerkleHasher
from pymerkle.hasher import MerkleHasher

class MerkleTreeService:
    #Helper function
    def seralizeTransaction(self, tx):
        return json.dumps(tx.jsonData, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')



    def buildMerkleTree(self):
        tree = InmemoryTree(algorithm='sha256') #initilise a in memory tree

        #Fetches transactions by id and created at using iterators. sorted by crated at, ties are broken by id
        transactions = list(Transaction.objects.order_by("createdAt", "id").iterator())       
        for transaction in transactions: 
            tree.append_entry(self.seralizeTransaction(transaction))
        return tree, transactions

   


    #This function update the root hash in the model + updates hte leaf hashes in the model 
    def finaliseLedger(self):        
        tree, transactions = self.buildMerkleTree()
        rootHash = tree.get_state().hex() #initiliase root thash

        #Loop through and get leaf hashes and root hashes
        for i, tx in enumerate(transactions, start = 1):
            tx.merkleLeafHash = tree.get_leaf(i).hex()
            tx.merkleRootHash = rootHash #Adds merkle root hash to every transaction

        with db_transaction.atomic():
            Transaction.objects.bulk_update(transactions, ['merkleLeafHash', 'merkleRootHash']) 
 
        return rootHash
    




    def merkleProof(self, ID):
        tx = Transaction.objects.get(id=ID)
        hasher = MerkleHasher('sha256')
        recomputedLeaf = hasher.hash_buff(self.seralizeTransaction(tx))
        return recomputedLeaf == bytes.fromhex(tx.merkleLeafHash)