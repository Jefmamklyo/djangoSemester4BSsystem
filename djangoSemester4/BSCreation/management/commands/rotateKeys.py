import json

from django.core.management.base import BaseCommand
from django.db import transaction
from cryptography.fernet import Fernet, MultiFernet

from BSCreation.crypt import getKeyFile, loadKeys
from BSCreation.physicalEntrophy import OSRandSource, CamSource, deriveKey 
from BSCreation.models import UserAccount


class Command(BaseCommand):
    help = "Generate and (rotate) keys"

    def add_arguments(self, parser):
        parser.add_argument("--source", choices=["webcam", "os"], default="webcam")


    def handle(self, *args, **opts):
      source = [OSRandSource()]
      if opts["source"] == "webcam":
          source.insert(0, CamSource())


      #key instantiaon and loading
      keys = [deriveKey(source).decode()] + loadKeys()
      getKeyFile().write_text(json.dumps(keys))  

      #encryption with changed keys
      cryptogReassign = MultiFernet([Fernet(k) for k in keys]) #create and group fernet keys together

      with transaction.atomic():
          #change all users thing re encryption
          accounts = list(UserAccount.objects.select_for_update())

          for account in accounts:
               #multifernet implicit key rotation
              account.encryptedBalance = cryptogReassign.rotate(account.encryptedBalance.encode()).decode()
              account.encryptedAccountID = cryptogReassign.rotate(account.encryptedAccountID.encode()).decode()
          UserAccount.objects.bulk_update(accounts, ["encryptedBalance", "encryptedAccountID"])

      self.stdout.write(self.style.SUCCESS(f"Keys rotated on accounts. Total accounts = {len(accounts)}, the accounts are {list(accounts)}"))
