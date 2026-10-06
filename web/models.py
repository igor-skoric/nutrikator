from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=120, default="Nutrikator")
    legal_name = models.CharField(max_length=200, blank=True)
    tagline = models.TextField(blank=True)
    pib = models.CharField(max_length=32, blank=True)
    maticni_broj = models.CharField(max_length=32, blank=True)
    email_info = models.EmailField(blank=True)
    email_privacy = models.EmailField(blank=True)
    phone_sales = models.CharField(max_length=64, blank=True)
    phone_office = models.CharField(max_length=64, blank=True)
    founder_name = models.CharField(max_length=120, blank=True)
    founder_title = models.CharField(max_length=200, blank=True)
    address_footer = models.TextField(blank=True)
    method = models.JSONField(default=dict, blank=True)
    funding = models.TextField(blank=True)
    raw = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name_plural = "Company"

    def __str__(self):
        return self.name


class SiteContent(models.Model):
    """Homepage and shared page copy from scraped home.json."""

    key = models.SlugField(unique=True, default="home")
    data = models.JSONField(default=dict)

    def __str__(self):
        return self.key


class Package(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=80)
    subtitle = models.CharField(max_length=200, blank=True)
    price = models.PositiveIntegerField()
    currency = models.CharField(max_length=8, default="RSD")
    featured = models.BooleanField(default=False)
    color = models.CharField(max_length=20, blank=True)
    cta = models.CharField(max_length=120, blank=True)
    features = models.JSONField(default=list)
    sample_report = models.URLField(blank=True)
    sample_label = models.URLField(blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "price"]

    def __str__(self):
        return f"{self.name} ({self.price} {self.currency})"


class Audience(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=200)
    image = models.CharField(max_length=300, blank=True, help_text="Static path or remote URL")
    intro = models.TextField(blank=True)
    lead = models.TextField(blank=True)
    services = models.JSONField(default=list, blank=True)
    paragraphs = models.JSONField(default=list, blank=True)
    outro = models.TextField(blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "title"]

    def __str__(self):
        return self.title


class FAQ(models.Model):
    slug = models.SlugField(unique=True)
    question = models.CharField(max_length=300)
    answer = models.JSONField(default=list, help_text="List of paragraphs")
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question


class LegalPage(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=200)
    body_md = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class OrderFormField(models.Model):
    field_id = models.SlugField(unique=True)
    label = models.CharField(max_length=200)
    field_type = models.CharField(max_length=40)
    options = models.JSONField(default=list, blank=True)
    hint = models.TextField(blank=True)
    required = models.BooleanField(default=True)
    multiple = models.BooleanField(default=False)
    sort_order = models.PositiveSmallIntegerField(default=0)
    raw = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.label
