FROM python:3.11-slim

ARG AMASS_VERSION=5.0.1

# Install system dependencies and Go toolchain for building Amass
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      ca-certificates \
      curl \
      git \
      build-essential \
      golang && \
    rm -rf /var/lib/apt/lists/*

# Build Amass from source
RUN git clone --branch v${AMASS_VERSION} --depth 1 https://github.com/owasp-amass/amass.git /tmp/amass && \
    cd /tmp/amass && \
    go build -o /usr/local/bin/amass ./cmd/amass && \
    rm -rf /tmp/amass

WORKDIR /app

# Install Python deps
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

ENV HOST=0.0.0.0
EXPOSE 8000

CMD ["python", "server.py"]
