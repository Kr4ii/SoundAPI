FROM python:3.9

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    ffmpeg \
    libsndfile1 \
    gcc \
    python3-dev && \
    apt-get clean

COPY ./app /app

ENV PYTHONPATH=/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Command to start
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
