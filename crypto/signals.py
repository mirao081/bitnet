print("✅ crypto.signals loaded")  

from django.db.models.signals import post_save
from django.dispatch import receiver
from crypto.models import Wallet, TokenSaleSection

@receiver(post_save, sender=Wallet)
def update_token_sale(sender, instance, **kwargs):
    print("🔥 Signal fired for Wallet:", instance.id)  
    total = sum(w.balance for w in Wallet.objects.all())
    sale = TokenSaleSection.objects.last()
    if sale:
        sale.contribution_received = total
        sale.save()
        print("💰 Updated contribution_received:", sale.contribution_received)
