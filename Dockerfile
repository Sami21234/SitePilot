
# # Using lightweight Python base image
# FROM python:3.11-slim

# # Setting working directory inside the container
# WORKDIR /app

# # Copying requirements file and installing dependencies
# COPY requirements.txt .

# # Install Python dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Copying the rest of the application code into the container
# COPY . .

# # Exposing the port on which the application will run
# # Default to 8000 if not set
# ENV PORT=8000

# # Expose the port (documentation, not enforcement)
# EXPOSE 8000

# # Command to run the application
# CMD uvicorn backend.main:app --host 0.0.0.0 --port $PORT

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

# Install torch separately first using CPU-only wheel
# This is cached as its own layer
RUN pip install --no-cache-dir --timeout=600 \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    torch==2.12.0

# Install everything else
RUN pip install --no-cache-dir --timeout=600 -r requirements.txt

COPY . .

ENV PORT=8000
EXPOSE 8000

CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port $PORT"]