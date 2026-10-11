FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install --extra-index-url https://download.pytorch.org/whl/cpu .[dev]

CMD ["celery", "-A", "app.tasks.celery_app", "worker", "--loglevel=info"]
