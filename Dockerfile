FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

ADD . /app

WORKDIR /app

RUN uv sync --locked

RUN echo "Applying database migrations..."
RUN uv run manage.py migrate

RUN echo "Seeding database..."
RUN uv run manage.py seedapp

CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:8000", "inventio_backend.wsgi:application"]