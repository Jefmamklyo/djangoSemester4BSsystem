from .models import Transaction
from .service import MerkleTreeService
from django.dispatch import receiver
from django.db.models.signals import post_save

@receiver(post_save, sender=Transaction)
def hashTransaction (sender, instance, created, **kwargs):
    if created:
        MerkleTreeService().finaliseLedger()
