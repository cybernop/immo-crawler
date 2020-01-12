FROM python:3.7 AS builder

WORKDIR /crawler

COPY immocrawler/ immocrawler/
COPY setup.py .

RUN python setup.py sdist bdist_wheel

#######

FROM python:3.7-alpine

WORKDIR /crawler

COPY main.py .

COPY --from=builder /crawler/dist/ dist/

RUN apk add --no-cache --virtual .build-deps \
    build-base \
    libstdc++ \
    libffi-dev \
    libressl-dev \
    && pip install dist/immocrawler-0.1-py3-none-any.whl \
    && apk del .build-deps

RUN mkdir /data /cfg

ENTRYPOINT ["python", "main.py", "--data-dir", "/data", "--config", "/cfg/config.yml"]
