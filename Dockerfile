FROM python:2

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY sau /app/sau
COPY sausite /app/sausite

COPY run.sh /run.sh

EXPOSE 8000

ENV PYTHONPATH /app:/configs
ENV DJANGO_SETTINGS_MODULE sausite.settings

CMD ["/run.sh"]
