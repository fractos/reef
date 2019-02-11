FROM alpine:3.6

RUN apk add --update --no-cache --virtual=run-deps \
  python3-dev \
  ca-certificates \
  py3-psycopg2 \
  uwsgi \
  uwsgi-http \
  uwsgi-python3 \
  vim \
  build-base \
  libxslt-dev \
  libxml2-dev

ENV SLEEP_SECONDS 60
ENV DB_NAME reef.db
ENV DB_TYPE sqlite

WORKDIR /opt/app
CMD ["python3", "-u", "reef.py"]

COPY requirements.txt /opt/app/
RUN pip3 install --no-cache-dir -r /opt/app/requirements.txt

COPY app /opt/app/
# COPY config /opt/app/config
# ENV CONFIG_FILE config/queries.json
# ENV DEBUG True
