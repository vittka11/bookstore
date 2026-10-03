FROM python:3.14-slim

WORKDIR /app

# gettext нужен Django для создания .po и .mo файлов
RUN apt-get update \
    && apt-get install -y --no-install-recommends gettext \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN chmod +x /app/docker-entrypoint.sh

ENTRYPOINT ["/app/docker-entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]