FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install --extra-index-url https://download.pytorch.org/whl/cpu .[dev]

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:create_app()"]
