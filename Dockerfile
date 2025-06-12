FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN apt-get update && apt-get install -y tesseract-ocr libgl1
RUN pip install -r backend/requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]