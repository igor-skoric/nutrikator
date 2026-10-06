from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Audience, Company, FAQ, LegalPage, Package, SiteContent


def _base_context():
    company = Company.objects.first()
    site = SiteContent.objects.filter(key="home").first()
    return {
        "company": company,
        "home_content": site.data if site else {},
    }


def home(request):
    ctx = _base_context()
    ctx["packages"] = Package.objects.all()
    return render(request, "home.html", ctx)


def page_o_nama(request):
    ctx = _base_context()
    ctx["page_title"] = "O nama"
    return render(request, "pages/o_nama.html", ctx)


def page_benefiti(request):
    ctx = _base_context()
    ctx["page_title"] = "Benefiti"
    return render(request, "pages/benefiti.html", ctx)


def page_vs_laboratorija(request):
    ctx = _base_context()
    ctx["page_title"] = "Nutrikator vs laboratorijska analiza"
    return render(request, "pages/vs_laboratorija.html", ctx)


def page_usluge(request):
    ctx = _base_context()
    ctx["page_title"] = "Usluge"
    ctx["audiences"] = Audience.objects.all()
    return render(request, "pages/usluge.html", ctx)


def page_paketi(request):
    ctx = _base_context()
    ctx["page_title"] = "Paketi"
    ctx["packages"] = Package.objects.all()
    return render(request, "pages/paketi.html", ctx)


def page_kako_naruciti(request):
    ctx = _base_context()
    ctx["page_title"] = "Kako naručiti"
    return render(request, "pages/kako_naruciti.html", ctx)


def page_faq(request):
    ctx = _base_context()
    ctx["page_title"] = "FAQ"
    ctx["faqs"] = FAQ.objects.all()
    return render(request, "pages/faq.html", ctx)


def legal_page(request, slug):
    page = get_object_or_404(LegalPage, slug=slug)
    ctx = _base_context()
    ctx["page"] = page
    return render(request, "legal.html", ctx)


def robots(request):
    site = settings.SITE_URL.rstrip("/")
    body = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /admin/\n"
        "\n"
        f"Sitemap: {site}/sitemap.xml\n"
    )
    return HttpResponse(body, content_type="text/plain; charset=utf-8")


def sitemap_xml(request):
    names = [
        ("home", "1.0"),
        ("usluge", "0.9"),
        ("paketi", "0.9"),
        ("kako_naruciti", "0.8"),
        ("faq", "0.8"),
        ("benefiti", "0.7"),
        ("vs_laboratorija", "0.7"),
        ("o_nama", "0.6"),
        ("uslovi", "0.3"),
        ("privatnost", "0.3"),
        ("kolacici", "0.2"),
    ]
    site = settings.SITE_URL.rstrip("/")
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for name, priority in names:
        loc = site + reverse(name)
        lines.append(
            f"<url><loc>{loc}</loc><changefreq>weekly</changefreq><priority>{priority}</priority></url>"
        )
    lines.append("</urlset>")
    return HttpResponse("\n".join(lines), content_type="application/xml; charset=utf-8")
