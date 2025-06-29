FROM python:3.9-slim
RUN apt-get update && apt-get install -y \
    python3-pygame \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libxrandr2 \
    libxtst6 \
    libxi6 \
    libgl1 \
    libpulse0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV DISPLAY=:0
CMD ["python", "main.py"]