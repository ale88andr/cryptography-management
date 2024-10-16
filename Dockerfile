FROM python:3.11.9-slim

RUN apt update && apt install -y --no-install-recommends locales; rm -rf /var/lib/apt/lists/*; sed -i '/^#.* ru_RU.UTF-8 /s/^#//' /etc/locale.gen; locale-gen
RUN locale -a

COPY src/requirements.txt src/requirements.txt

# Install dependencies
# RUN apt install -y \
#     build-essential \
#     libpq-dev \
#     postgresql-server-dev-all

# Restore backup
# cat your_dump.sql | docker exec -i your-db-container psql -U postgres

RUN pip install -r src/requirements.txt

COPY . .

CMD [ "python", "src/main.py" ]