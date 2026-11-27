"""Load the starter portfolio so the page is not empty on a fresh install.

    python manage.py seed_portfolio

Safe to run more than once: items that already exist (same title and
category) are skipped. After seeding, edit or delete them in /admin/.
"""
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from TechApp.content import DESIGNS, PROJECTS
from TechApp.models import PortfolioItem


class Command(BaseCommand):
    help = "Create starter portfolio items from TechApp/content.py"

    def handle(self, *args, **options):
        created = 0

        for i, p in enumerate(PROJECTS):
            _, made = PortfolioItem.objects.get_or_create(
                title=p["name"], category=PortfolioItem.WEB,
                defaults={
                    "tag": p["industry"],
                    "summary": p["summary"],
                    "stack": ", ".join(p["stack"]),
                    "url": p["url"],
                    "order": i,
                },
            )
            created += made

        static_dir = Path(settings.BASE_DIR) / "static"
        for i, d in enumerate(DESIGNS):
            if PortfolioItem.objects.filter(title=d["title"], category=PortfolioItem.DESIGN).exists():
                continue
            item = PortfolioItem(
                title=d["title"], category=PortfolioItem.DESIGN, tag=d["type"],
                summary=d["brief"], notes=d["notes"], order=i,
            )
            src = static_dir / d["image"]
            if src.exists():
                with src.open("rb") as fh:
                    item.image.save(src.name, File(fh), save=False)
            item.save()
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Portfolio seeded: {created} new item(s)."))
