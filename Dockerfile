FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install basic utilities required for .deb installs
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Copy deb packages and install tesseract-related .deb files (OFFLINE)
COPY deb_packages/ /app/deb_packages/
RUN apt-get update && \
    dpkg -i /app/deb_packages/*.deb || apt-get -f install -y && \
    rm -rf /var/lib/apt/lists/*

# Copy Python wheels and install Python dependencies OFFLINE
COPY wheels/ ./wheels/
COPY requirements.txt .
RUN pip install --no-cache-dir --no-index --find-links=./wheels -r requirements.txt

# Copy the rest of your code
COPY . .

# Run the script
CMD ["python", "main.py"]

