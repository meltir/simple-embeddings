FROM --platform=${BUILDPLATFORM} python:slim-buster
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

RUN apt update \
    && apt install -y cmake pkg-config build-essential
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu \
    && pip install -r requirements.txt

RUN apt remove -y cmake pkg-config build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*