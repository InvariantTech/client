ARG TARGETPLATFORM
FROM python:3.12-slim@sha256:4718a47de1298c890b835bd5f4978acee04ba90f17c3395ee3d5e06920b63a26

ARG INVARIANT_VERSION
ARG BUILD_DATE
ARG VCS_REF

LABEL tech.invariant.client.version="${INVARIANT_VERSION}"
LABEL python_version="3.12"

LABEL org.opencontainers.image.description="Invariant CLI: Network Security Access Policy"
LABEL org.opencontainers.image.documentation="https://github.com/InvariantTech/client/blob/main/README.md"
LABEL org.opencontainers.image.base.name="python:3.12-slim@sha256:4718a47de1298c890b835bd5f4978acee04ba90f17c3395ee3d5e06920b63a26"
LABEL org.opencontainers.image.base.digest="sha256:4718a47de1298c890b835bd5f4978acee04ba90f17c3395ee3d5e06920b63a26"
LABEL org.opencontainers.image.created="${BUILD_DATE}"
LABEL org.opencontainers.image.revision="${VCS_REF}"
LABEL org.opencontainers.image.version="${INVARIANT_VERSION}"

WORKDIR /data

RUN pip3 install invariant-client==${INVARIANT_VERSION}

ENTRYPOINT ["invariant"]
