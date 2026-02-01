FROM smart-ml-base:cpu

WORKDIR /app
ENV PYTHONPATH=/app

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY backend /app/backend

RUN mkdir -p /app/uploads /app/.easyocr /app/.models

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
