#!/usr/bin/env sh
set -e

echo "==> Running migrations"
python manage.py migrate --noinput

echo "==> Collect static"
python manage.py collectstatic --noinput

exec "$@"