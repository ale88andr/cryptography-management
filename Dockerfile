FROM python:3.11.9-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

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

RUN pip install --no-cache-dir --upgrade -r src/requirements.txt

COPY . .

RUN chmod +x docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]

CMD [ "python", "src/main.py" ]