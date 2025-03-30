FROM python:3.9-slim

WORKDIR /app

# ��������� ��������� ������������
RUN apt-get update && \
    apt-get install -y ffmpeg libsndfile1 && \
    apt-get clean

COPY requirements.txt .

# ��������� Python-������������
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app

# �������� ������� ����������
RUN mkdir -p /data/temp /data/output /app/logs

# ������� �������
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
