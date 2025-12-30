FROM python:3.11-slim

ARG AMASS_VERSION=4.2.0

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      ca-certificates \
      curl \
      unzip \
      git && \
    rm -rf /var/lib/apt/lists/*

# Install Amass binary (prebuilt)
RUN curl -sSfL "https://github.com/owasp-amass/amass/releases/download/v${AMASS_VERSION}/amass_Linux_amd64.zip" -o /tmp/amass.zip && \
    unzip /tmp/amass.zip -d /tmp/amass && \
    mv /tmp/amass/amass_Linux_amd64/amass /usr/local/bin/amass && \
    chmod +x /usr/local/bin/amass && \
    rm -rf /tmp/amass /tmp/amass.zip

WORKDIR /app

# Install Python deps
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

ENV HOST=0.0.0.0
EXPOSE 8000

CMD ["python", "server.py"]
