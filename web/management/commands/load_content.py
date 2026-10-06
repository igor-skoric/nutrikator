"""Load scraped Nutrikator content from data/content into the database."""

from __future__ import annotations

import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from web.models import (
    Audience,
    Company,
    FAQ,
    LegalPage,
    OrderFormField,
    Package,
    SiteContent,
)

CONTENT_DIR = Path(settings.BASE_DIR) / "data" / "content"

LEGAL_FILES = {
    "politika-privatnosti": ("Politika privatnosti", "legal/politika-privatnosti.md"),
    "uslovi-poslovanja": ("Uslovi poslovanja", "legal/uslovi-poslovanja.md"),
    "politika-upotrebe-kolacica": (
        "Politika upotrebe kolačića",
        "legal/politika-upotrebe-kolacica.md",
    ),
}


def _load_json(name: str) -> dict | list:
    path = CONTENT_DIR / name
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


class Command(BaseCommand):
    help = "Import scraped JSON/MD content from data/content into Django models."

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete existing content rows before import.",
        )

    def handle(self, *args, **options):
        if options["flush"]:
            self.stdout.write("Flushing existing content…")
            Package.objects.all().delete()
            Audience.objects.all().delete()
            FAQ.objects.all().delete()
            OrderFormField.objects.all().delete()
            LegalPage.objects.all().delete()
            SiteContent.objects.all().delete()
            Company.objects.all().delete()

        self._load_company()
        self._load_home()
        self._load_packages()
        self._load_audiences()
        self._load_faq()
        self._load_order_form()
        self._load_legal()
        self.stdout.write(self.style.SUCCESS("Content import complete."))

    def _load_company(self):
        data = _load_json("company.json")
        emails = data.get("emails") or {}
        phones = data.get("phones") or {}
        founder = data.get("founder") or {}
        addresses = data.get("addresses") or {}
        footer = (addresses.get("currentFooter") or {}).get("value", "")

        obj, created = Company.objects.update_or_create(
            pk=1,
            defaults={
                "name": data.get("name", "Nutrikator"),
                "legal_name": data.get("legalName", ""),
                "tagline": data.get("tagline", ""),
                "pib": data.get("pib", ""),
                "maticni_broj": data.get("maticniBroj", ""),
                "email_info": emails.get("info", ""),
                "email_privacy": emails.get("privacy", ""),
                "phone_sales": phones.get("sales", ""),
                "phone_office": phones.get("office", ""),
                "founder_name": founder.get("name", ""),
                "founder_title": founder.get("title", ""),
                "address_footer": footer,
                "method": data.get("method") or {},
                "funding": data.get("funding", ""),
                "raw": data,
            },
        )
        self.stdout.write(f"  Company: {'created' if created else 'updated'}")

    def _load_home(self):
        data = _load_json("home.json")
        obj, created = SiteContent.objects.update_or_create(
            key="home",
            defaults={"data": data},
        )
        self.stdout.write(f"  SiteContent(home): {'created' if created else 'updated'}")

    def _load_packages(self):
        data = _load_json("packages.json")
        packages = data.get("current") or []
        for i, pkg in enumerate(packages):
            Package.objects.update_or_create(
                slug=pkg["id"],
                defaults={
                    "name": pkg.get("name", pkg["id"]),
                    "subtitle": pkg.get("subtitle", ""),
                    "price": pkg.get("price", 0),
                    "currency": pkg.get("currency", "RSD"),
                    "featured": bool(pkg.get("featured")),
                    "color": pkg.get("color", ""),
                    "cta": pkg.get("cta", ""),
                    "features": pkg.get("features") or [],
                    "sample_report": pkg.get("sampleReport") or "",
                    "sample_label": pkg.get("sampleLabel") or "",
                    "sort_order": i,
                },
            )
        self.stdout.write(f"  Packages: {len(packages)}")

    def _load_audiences(self):
        data = _load_json("audiences.json")
        items = data.get("items") or []
        for i, item in enumerate(items):
            Audience.objects.update_or_create(
                slug=item["id"],
                defaults={
                    "title": item.get("title", item["id"]),
                    "image": item.get("image", ""),
                    "intro": item.get("intro", ""),
                    "lead": item.get("lead", ""),
                    "services": item.get("services") or [],
                    "paragraphs": item.get("paragraphs") or [],
                    "outro": item.get("outro", ""),
                    "sort_order": i,
                },
            )
        self.stdout.write(f"  Audiences: {len(items)}")

    def _load_faq(self):
        data = _load_json("faq.json")
        items = data.get("items") or []
        for i, item in enumerate(items):
            FAQ.objects.update_or_create(
                slug=item["id"],
                defaults={
                    "question": item.get("question", item["id"]),
                    "answer": item.get("answer") or [],
                    "sort_order": i,
                },
            )
        self.stdout.write(f"  FAQs: {len(items)}")

    def _load_order_form(self):
        data = _load_json("order-form.json")
        fields = data.get("requiredFromClient") or []
        for i, field in enumerate(fields):
            OrderFormField.objects.update_or_create(
                field_id=field["id"],
                defaults={
                    "label": field.get("label", field["id"]),
                    "field_type": field.get("type", "text"),
                    "options": field.get("options") or [],
                    "hint": field.get("hint", ""),
                    "required": not field.get("optional", False),
                    "multiple": bool(field.get("multiple")),
                    "sort_order": i,
                    "raw": field,
                },
            )
        self.stdout.write(f"  Order form fields: {len(fields)}")

    def _load_legal(self):
        count = 0
        for slug, (title, rel) in LEGAL_FILES.items():
            path = CONTENT_DIR / rel
            if not path.exists():
                self.stderr.write(f"  Missing legal file: {rel}")
                continue
            body = path.read_text(encoding="utf-8")
            LegalPage.objects.update_or_create(
                slug=slug,
                defaults={"title": title, "body_md": body},
            )
            count += 1
        self.stdout.write(f"  Legal pages: {count}")
