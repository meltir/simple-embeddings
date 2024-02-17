FROM --platform=${BUILDPLATFORM} python:slim-buster

LABEL org.opencontainers.image.source="https://github.com/meltir/simple-embeddings" \
      org.opencontainers.image.version="0.0.1" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.description="Simple embedding endpoint" \
      org.opencontainers.image.vendor="meltir" \
      org.opencontainers.image.maintainers="spam@meltir.com" \
      org.opencontainers.image.created="2024-02-18T00:00:00Z"

LABEL authors="spam@meltir.com"
LABEL maintainer="Lukasz Andrzejak"
LABEL description="Simple embedding endpoint"
ENV TZ="Europe/London"
ENV HF_HOME=/app/hf_cache/

EXPOSE 5000
WORKDIR /app
ENTRYPOINT ["flask", "run", "--host=0.0.0.0"]

RUN mkdir -p /app/hf_cache \
    && chmod 777 -R /app

COPY . .

RUN pip install torch --index-url https://download.pytorch.org/whl/cpu

RUN apt update \
    && apt install -y cmake pkg-config build-essential \
    && pip install -r requirements.txt \
    && apt remove -y cmake pkg-config build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

