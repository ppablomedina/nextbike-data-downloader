FROM python:3.11-slim

# Evitar prompts interactivos
ENV DEBIAN_FRONTEND=noninteractive

# 1. Instalar dependencias del sistema + Chromium + Chromedriver
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    fonts-liberation \
    libnss3 \
    libasound2 \
    libxss1 \
    libatk1.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxtst6 \
    libxrandr2 \
    libgbm1 \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 2. Variables para que Selenium encuentre Chromium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# 3. Instalar dependencias Python
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar el código
COPY . .

# 5. Puerto para Cloud Run / Functions
ENV PORT=8080

# 6. Comando de arranque
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
