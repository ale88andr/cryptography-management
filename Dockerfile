FROM python:3.11.9-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV http_proxy=http://10.92.239.85:3128
ENV https_proxy=http://10.92.239.85:3128

COPY src/requirements.txt src/requirements.txt

# Install dependencies
RUN apt update && apt install -y --no-install-recommends locales; rm -rf /var/lib/apt/lists/*; sed -i '/^#.* ru_RU.UTF-8 /s/^#//' /etc/locale.gen; locale-gen \
    apt install -y \
    build-essential \
    libpq-dev \
    postgresql-server-dev-all \
    locale -a

# Restore backup
# cat your_dump.sql | docker exec -i your-db-container psql -U postgres

RUN pip install --no-cache-dir -r src/requirements.txt

COPY . .
