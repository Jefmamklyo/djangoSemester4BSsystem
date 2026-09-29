import hashlib
from cryptography.fernet import Fernet, MultiFernet

from django.conf import settings

import json
from pathlib import Path


def getKeyFile():
    return Path(getattr(settings, "FERNET_KEYFILE", Path(settings.BASE_DIR) / "fernet_keys.json"))

def loadKeys():
    if getKeyFile().exists():
        return json.loads(getKeyFile().read_text()) #returnn key file 
    key = settings.FERNET_ENCRYPT_KEY

    if isinstance(key,bytes): #null checking
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
    
