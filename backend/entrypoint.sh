#!/bin/sh
set -e

# Migrations (--noinput évite EOFError quand aucun TTY, ex. Docker)
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Fichiers statiques (admin Django)
python manage.py collectstatic --noinput --clear

# Créer le superuser si les variables sont définies
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  python manage.py createsuperuser --noinput 2>/dev/null || true
fi

exec "$@"
