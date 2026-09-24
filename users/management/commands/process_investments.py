from django.core.management.base import BaseCommand

from users.utils import process_matured_investments


class Command(BaseCommand):
    help = "Process investment payouts and complete matured investments."

    def handle(self, *args, **options):
        processed = process_matured_investments()

        self.stdout.write(
            self.style.SUCCESS(
                f"{processed} investment payout(s)/completion(s) processed."
            )
        )