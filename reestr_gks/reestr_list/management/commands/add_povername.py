from typing import Any
from django.core.management import BaseCommand
from reestr_list.models import Pover


class Command(BaseCommand):
    """
    Add povername to model Pover
    """

    def handle(self, *args, **options) -> str | None:
        self.stdout.write('Add povername...')
        povernames = [
            "Киселев К.А.",
            "Якимов А.С.",
            "Габдельхаков М.И.",
            "Малышев Р.С.",
            "Ульянов В.В.",
        ]
        for pover_name in povernames:
            povers, created = Pover.objects.get_or_create(povername=pover_name)
            self.stdout.write(f"Добавлены поверители {povers.povername}")

        self.stdout.write(self.style.SUCCESS("Povername added"))
