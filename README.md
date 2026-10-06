# Nutrikator (Django)

Django projekat sa sadržajem sa scrapovanog sajta (`data/content/`) i početnom stranicom iz `nutrikator-demo/index2.html` (`templates/home.html`).

## Pokretanje

```bash
cd D:\projects\nutrikator-django
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py load_content
python manage.py runserver
```

- Početna: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Struktura

- `config/` — Django settings / URLs
- `web/` — modeli, views, `load_content` management command
- `templates/home.html` — hero iz index2.html
- `static/img/` — logo i slike
- `data/content/` — JSON + legal MD iz scrapinga

## Import sadržaja

```bash
python manage.py load_content --flush
```

Učitava company, home, pakete (6k/8k/12k), audience, FAQ, order-form polja i legal stranice.

## Produkcija

Dozvoljeni hostovi: `nutrikator.rs`, `www.nutrikator.rs`, `nutrikator.rs.itbranch.rs`.

Na serveru kopiraj `.env.example` u `.env`, postavi `DJANGO_SECRET_KEY` i `DJANGO_DEBUG=false`, pa:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py load_content
python manage.py collectstatic --noinput
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

Proxy treba da prosleđuje `X-Forwarded-Proto: https`. `DJANGO_SECURE_SSL_REDIRECT=true` uključi tek kada je to provereno, da ne nastane petlja preusmeravanja.
