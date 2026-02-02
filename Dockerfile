FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y ffmpeg curl
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app ./app
CMD ["python", "app/web.py"]
