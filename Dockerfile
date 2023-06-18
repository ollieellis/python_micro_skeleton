FROM python:3.11

WORKDIR /app

COPY requirements_prod.txt .
COPY main.py .

#this needs to be removed and passed into the volume using a config map
COPY config/config.yaml ./config/config.yaml

RUN pip install --no-cache-dir -r requirements_prod.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]