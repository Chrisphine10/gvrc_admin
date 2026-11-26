from django.core.management.base import BaseCommand

from apps.sms.services import process_pending_broadcasts


class Command(BaseCommand):
    help = (
        "Send any queued bulk SMS. Broadcasts normally send in the background "
        "right after they are created; run this every minute from cron or a "
        "systemd timer so a broadcast interrupted by a restart still finishes."
    )

    def handle(self, *args, **options):
        totals = process_pending_broadcasts()
        self.stdout.write(
            f"broadcasts={totals['broadcasts']} sent={totals['sent']} failed={totals['failed']}"
        )
