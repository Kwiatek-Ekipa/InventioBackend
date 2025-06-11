#!/bin/sh

set -e

# Wykonaj migracje bazy danych
echo "Applying database migrations..."
uv run manage.py migrate

# Wykonaj seedowanie bazy danych (opcjonalne)
echo "Seeding database..."
uv run manage.py seedapp

# Uruchom główne polecenie (CMD z Dockerfile)
exec "$@"