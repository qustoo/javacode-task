FROM python:3.10-slim

WORKDIR /app


COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .
COPY .env .

ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8080
RUN chmod +x wait-for-db.sh

CMD ["sh","-c","./wait-for-db.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]