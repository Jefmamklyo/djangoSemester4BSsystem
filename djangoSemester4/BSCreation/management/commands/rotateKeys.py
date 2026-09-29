import json

from django.core.management.base import BaseCommand
from django.db import transaction
from cryptography.fernet import Fernet, MultiFernet

from BSCreation.crypt import keyfile, loadKeys
from BSCreation.physicalEntrophy import OSRandSource, CamSource, deriveKey 
from BSCreation.models import UserAccount


class Command(BaseCommand):
    help = "Generate and rotate keys"

    def add_arguments(self, parser):
        parser.add_argument("--source", choices=["webcam", "os"], default="webcam")


    def handle(self, *args, **opts):
      