FROM python:3.9.5-alpine3.13

RUN set -eux; \
    apk add --update --no-cache \
        bash \
        openssh-client \
        make \
        git \
        openjdk8-jre \
        ttf-dejavu \
        graphviz \
    ;

RUN set -eux; \
    mkdir /design; \
    ln -s /design /var/design

COPY ./docs-creation/requirements.txt /requirements.txt
RUN set -eux; \
    python -m pip install -r /requirements.txt

WORKDIR /design
COPY . /design
