#!/bin/sh

set -e

echo "Applying database migrations..."
uv run manage.py migrate

echo "Seeding database..."
uv run manage.py seedapp

exec "$@"