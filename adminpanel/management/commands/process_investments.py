# adminpanel/management/commands/process_investments.py

from django.core.management.base import BaseCommand
from users.utils import process_matured_investments  # ✅ import the reusable function

class Command(BaseCommand):
    help = "Process matured investments and credit user balances"

    def handle(self, *args, **kwargs):
        # Call the function from utils
        process_matured_investments()

        # Print a success message to the console/logs
        self.stdout.write(self.style.SUCCESS("Processed matured investments"))
