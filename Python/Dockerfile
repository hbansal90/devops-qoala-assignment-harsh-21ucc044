FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    net-tools \
    iproute2 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir flask netifaces gunicorn

COPY app.py .

EXPOSE 8001

# Command to run the application with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8001", "app:app"]