FROM python:3.12-slim

ARG INVARIANT_VERSION
ARG PYTHON_VERSION

LABEL invariant_client_version="${INVARIANT_VERSION}"
LABEL python_version="${PYTHON_VERSION}"

WORKDIR /data

RUN pip3 install invariant-client

ENTRYPOINT ["invariant"]
