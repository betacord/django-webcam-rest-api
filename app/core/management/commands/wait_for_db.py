import time

from django.core.management import BaseCommand
from django.db import connections, OperationalError


class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    def handle(self, *args: list, **options: dict) -> None:
        self.stdout.write('waiting for db...')
        db_conn = None

        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError as e:
                self.stdout.write(f'db unavailable: {e}, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available'))
