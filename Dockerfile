FROM python:3

COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r /app/requirements.txt
RUN apt-get update && apt-get install -y \
  nginx

COPY manage.py /app/
COPY sau /app/sau
COPY sausite /app/sausite
COPY sau/static /static

COPY run.sh /run.sh

EXPOSE 8000

ENV PYTHONPATH /app:/configs
ENV DJANGO_SETTINGS_MODULE sausite.settings

CMD ["/run.sh"]
