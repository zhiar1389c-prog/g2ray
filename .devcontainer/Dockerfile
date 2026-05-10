FROM debian:bookworm-slim

COPY install.sh /app/install.sh

WORKDIR /app

# Install dependencies with clear output
RUN echo "📦 Installing system dependencies..." && \
    apt-get update && apt-get install -y --no-install-recommends \
    bash git curl wget unzip tzdata openssl ca-certificates \
    python3 python3-pip python3-venv \
    && echo "✅ Dependencies installed successfully" \
    && rm -rf /var/lib/apt/lists/*

# Setup and configure xray
RUN echo "⚙️  Running installation script..." && \
    chmod +x /app/install.sh && /app/install.sh && \
    echo "✅ Installation completed successfully"

COPY config.json /etc/config.json

COPY requirements.txt /app/requirements.txt
COPY bot.py /app/bot.py

RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip install -r /app/requirements.txt

CMD ["/app/venv/bin/python", "/app/bot.py"]
