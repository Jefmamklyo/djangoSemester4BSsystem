import json
from os import O_ASYNC
from .models import Transaction
import pymerkle
from django.db import transaction as db_transaction


#Helper function
def seralize_transaction(tx):
    return json.dumps(tx.jsonData, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')

def buildMerkleTree():
    pass
    #build merkle tree using pymerkle and datafrom the transactioun at runtime


def finaliseLedger():
    pass
    #update a lot of things her

def merkleProof():
    pass
    #cerate a merkle proof algorith by rebulding the trees