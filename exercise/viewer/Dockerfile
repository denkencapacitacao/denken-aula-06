FROM python:3.11-alpine
RUN addgroup -g 1000 appgroup && adduser -D -u 1000 -G appgroup appuser
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY viewer.py .
RUN chown -R appuser:appgroup /app
USER appuser
CMD ["python", "viewer.py"]
