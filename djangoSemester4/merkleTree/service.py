import json
from .models import Transaction
from pymerkle import InmemoryTree, verify_inclusion
from django.db import transaction as db_transaction


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
        tree, transactions = self.buildMerkleTree()

        #Stores the id of transactions in chronological orderas it is a for loop
        transactionIds=[tx.id for tx in transactions]
        
        
        #Input to check if a specific transaction is valid (retrieve specfic transaction)
        transactionIndex = transactionIds.index(ID) + 1

        inclusionProof = tree.prove_inclusion(transactionIndex, tree.get_size())

        base = tree.get_leaf(transactionIndex)
        root = tree.get_state(tree.get_size())

        try:
            verify_inclusion(base, root, inclusionProof)
            return True
        except Exception as e:
            return False