import json

from django.conf import settings

from .seo import DEFAULT, PAGES


def _dumps(data):
    return json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")


def _site():
    return settings.SITE_URL.rstrip("/")


def _organization(site, company):
    name = company.name if company else "Nutrikator"
    legal = (company.legal_name if company and company.legal_name else "Nutrikator d.o.o.")
    email = company.email_info if company and company.email_info else "info@nutrikator.com"
    phone = company.phone_sales if company and company.phone_sales else "+381 60 130 82 30"
    address = company.address_footer if company and company.address_footer else "Beograd"
    org = {
        "@type": "ProfessionalService",
        "@id": f"{site}/#organization",
        "name": name,
        "legalName": legal,
        "url": f"{site}/",
        "logo": f"{site}/static/img/logo-dark.png",
        "image": f"{site}/static/img/logo-dark.png",
        "email": email,
        "telephone": phone,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": address,
            "addressLocality": "Beograd",
            "postalCode": "11000",
            "addressCountry": "RS",
        },
        "areaServed": {"@type": "Country", "name": "Srbija"},
        "description": DEFAULT["description"],
    }
    if company and company.founder_name:
        org["founder"] = {
            "@type": "Person",
            "name": company.founder_name,
            "jobTitle": company.founder_title or "Osnivač",
        }
    return org


def _faq_entities():
    from .models import FAQ

    entities = []
    for item in FAQ.objects.all():
        parts = item.answer if isinstance(item.answer, list) else [item.answer]
        text = " ".join(str(part).strip() for part in parts if str(part).strip())
        if not item.question or not text:
            continue
        entities.append(
            {
                "@type": "Question",
                "name": item.question,
                "acceptedAnswer": {"@type": "Answer", "text": text},
            }
        )
    return entities


def _offers(site):
    from .models import Package

    offers = []
    for package in Package.objects.all():
        offers.append(
            {
                "@type": "Offer",
                "name": f"{package.name} — nutritivna deklaracija",
                "description": package.subtitle,
                "price": str(package.price),
                "priceCurrency": package.currency or "RSD",
                "url": f"{site}/paketi#{package.slug}",
                "availability": "https://schema.org/InStock",
            }
        )
    return offers


def seo(request):
    match = getattr(request, "resolver_match", None)
    name = match.url_name if match else ""
    meta = dict(DEFAULT)
    meta.update(PAGES.get(name, {}))
    site = _site()
    canonical = site + (request.path or "/")
    meta["canonical"] = canonical
    meta["og_image"] = f"{site}/static/img/logo-dark.png"
    meta["robots"] = "index, follow, max-image-preview:large"

    graph = []
    try:
        from .models import Company

        company = Company.objects.first()
    except Exception:
        company = None

    if name and not (request.path or "").startswith("/admin"):
        graph.append(_organization(site, company))
        graph.append(
            {
                "@type": "WebSite",
                "@id": f"{site}/#website",
                "url": f"{site}/",
                "name": "Nutrikator",
                "inLanguage": "sr",
                "publisher": {"@id": f"{site}/#organization"},
            }
        )
        if meta.get("crumb"):
            graph.append(
                {
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {
                            "@type": "ListItem",
                            "position": 1,
                            "name": "Početna",
                            "item": f"{site}/",
                        },
                        {
                            "@type": "ListItem",
                            "position": 2,
                            "name": meta["crumb"],
                            "item": canonical,
                        },
                    ],
                }
            )
        try:
            if name == "faq":
                entities = _faq_entities()
                if entities:
                    graph.append({"@type": "FAQPage", "mainEntity": entities})
            elif name == "paketi":
                offers = _offers(site)
                if offers:
                    graph.append(
                        {
                            "@type": "OfferCatalog",
                            "name": "Paketi nutritivne deklaracije",
                            "itemListElement": offers,
                        }
                    )
        except Exception:
            pass

    meta["json_ld"] = _dumps({"@context": "https://schema.org", "@graph": graph}) if graph else ""
    return {"seo": meta}
