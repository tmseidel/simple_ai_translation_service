FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download model at build time (optional, can be done at runtime)
RUN python -c "from transformers import AutoTokenizer, AutoModelForSeq2SeqLM; \
    model_name = 'facebook/nllb-200-distilled-600M'; \
    print('Downloading model...'); \
    AutoTokenizer.from_pretrained(model_name); \
    AutoModelForSeq2SeqLM.from_pretrained(model_name); \
    print('Model downloaded successfully')"

# Copy application code
COPY app.py .

EXPOSE 5000

# Use gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--timeout", "300", "app:app"]
