import hashlib
from cryptography.fernet import Fernet, MultiFernet

from django.conf import settings

import json
from pathlib import Path


def getKeyFile():
     path = Path(settings.BASE_DIR) / "fernetKeys.json"

     if not path.exists():
         print("Instantiated new path at base directory")
         path.write_text(json.dumps({}))

     return path


def loadKeys():

    if getKeyFile().exists():
        return json.loads(getKeyFile().read_text()) #returnn key file 
    key = settings.FERNET_ENCRYPT_KEY

    
    key = key.decode()
    return [key]

def cryptConverter():
    return MultiFernet([Fernet(k) for k in loadKeys()])

def encrypt(plainText):
    encText= cryptConverter().encrypt(plainText.encode()).decode()
    return encText

def decrypt(encText):
    decText = cryptConverter().decrypt(encText.encode()).decode()
    return decText


def hashLookups(plainText):
    #create hash field with ield encrypt key and the plaintext
    hashedField = hashlib.sha256((plainText + settings.FERNET_ENCRYPT_KEY).encode()).hexdigest() 
    return hashedField
    
