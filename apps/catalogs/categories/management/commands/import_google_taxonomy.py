import urllib.request
import uuid

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from apps.catalogs.categories.models.category_profile import CategoryProfile

TAXONOMY_URL = "https://www.google.com/basepages/producttype/taxonomy-with-ids.en-US.txt"


class Command(BaseCommand):
    help = "Import official Google Product Taxonomy categories (5,595+ categories) into CategoryProfile."

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=0, help="Max categories to import (0 = all).")
        parser.add_argument("--file", type=str, default="", help="Optional local taxonomy .txt file path.")

    def handle(self, *args, **options):
        limit = options["limit"]
        local_file = options["file"].strip()

        if local_file:
            with open(local_file, "r", encoding="utf-8") as fh:
                lines = fh.readlines()
        else:
            self.stdout.write(f"Downloading taxonomy from {TAXONOMY_URL} ...")
            with urllib.request.urlopen(TAXONOMY_URL, timeout=30) as resp:
                lines = resp.read().decode("utf-8").splitlines()

        existing_names = set(CategoryProfile.objects.values_list("name", flat=True))
        existing_slugs = set(CategoryProfile.objects.values_list("slug", flat=True))
        to_create = []

        for raw in lines:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if " - " in line:
                tax_id, cat_path = line.split(" - ", 1)
            else:
                tax_id, cat_path = "", line

            cat_name = cat_path.strip()[:255]
            if not cat_name or cat_name in existing_names:
                continue

            base_slug = slugify(cat_name)[:240] or f"cat-{uuid.uuid4().hex[:6]}"
            slug = base_slug
            counter = 1
            while slug in existing_slugs:
                slug = f"{base_slug[:235]}-{counter}"
                counter += 1

            existing_names.add(cat_name)
            existing_slugs.add(slug)
            to_create.append(
                CategoryProfile(
                    name=cat_name,
                    slug=slug,
                    description=f"Google Product Taxonomy ID: {tax_id.strip()}" if tax_id else "",
                    is_active=True,
                )
            )
            if limit and len(to_create) >= limit:
                break

        if to_create:
            CategoryProfile.objects.bulk_create(to_create, batch_size=500, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f"Imported {len(to_create)} new categories cleanly."))