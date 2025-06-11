# Etap budowania
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

ADD . /app

WORKDIR /app

RUN chmod +x ./entrypoint.sh
RUN uv sync --locked

ENTRYPOINT ["./entrypoint.sh"]
CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:8000", "inventio_backend.wsgi:application"]