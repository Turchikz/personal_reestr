from typing import Any
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        self.stdout.write('Create example')

        self.stdout.write(self.style.SUCCESS("Example created"))
