FROM python:3.10-slim

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

# Fix: Show logs in docker
ENV PYTHONUNBUFFERED="true" 

CMD ["python", "app.py"]
