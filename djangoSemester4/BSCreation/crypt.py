import hashlib
from cryptography.fernet import Fernet
from django.conf import settings

#initilisae fenet and give it the key to accesses
f = Fernet(settings.FERNET_ENCRYPT_KEY)

def encrypt(plainText):
    encText= f.encrypt(plainText.encode().decode())
    return encText

def decrypt(encText):
    decText = f.decrypt(encText).decode()
    return decText


def hashLookups(plainText):
    #create hash field with ield encrypt key and the plaintext
    hashedField = hashlib.sha256((plainText + settings.FERNET_ENCRYPT_KEY).encode()).hexdigest() 
    return hashedField
    
