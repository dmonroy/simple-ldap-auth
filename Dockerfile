FROM dmonroy/alpine-python:2.7
RUN apk add --update \
    build-base \
    cyrus-sasl-dev \
    libldap \
    libsasl \
    libssl1.0 \
    openldap-dev \
    && rm /var/cache/apk/*

ADD ./ /app
RUN pip install -r /app/requirements.txt

EXPOSE 8080
CMD python /app/ldap_auth.py