
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

# Installing torch separately first using CPU-only wheel
# This is cached as its own layer
RUN pip install --no-cache-dir --timeout=600 \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    torch==2.12.0

# Installing everything else
RUN pip install --no-cache-dir --timeout=600 -r requirements.txt

# Installing Playwright browser binaries
RUN playwright install chromium
RUN playwright install-deps chromium

COPY . .

ENV PORT=8000
EXPOSE 8000

CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port $PORT"]