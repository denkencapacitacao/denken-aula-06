FROM python:3.11-alpine

RUN addgroup -g 1000 appgroup && adduser -D -u 1000 -G appgroup appuser

WORKDIR /app
COPY app.py .

RUN pip install flask

USER appuser

CMD ["python", "app.py"]
