from django.urls import path

from . import views

urlpatterns = [
    path("robots.txt", views.robots, name="robots"),
    path("sitemap.xml", views.sitemap_xml, name="sitemap"),
    path("", views.home, name="home"),
    path("o-nama", views.page_o_nama, name="o_nama"),
    path("benefiti", views.page_benefiti, name="benefiti"),
    path("vs-laboratorija", views.page_vs_laboratorija, name="vs_laboratorija"),
    path("usluge", views.page_usluge, name="usluge"),
    path("paketi", views.page_paketi, name="paketi"),
    path("kako-naruciti", views.page_kako_naruciti, name="kako_naruciti"),
    path("faq", views.page_faq, name="faq"),
    path("uslovi-poslovanja", views.legal_page, {"slug": "uslovi-poslovanja"}, name="uslovi"),
    path("politika-privatnosti", views.legal_page, {"slug": "politika-privatnosti"}, name="privatnost"),
    path(
        "politika-upotrebe-kolacica",
        views.legal_page,
        {"slug": "politika-upotrebe-kolacica"},
        name="kolacici",
    ),
]
