# Agentic Legal Assistant - Hackathon Dockerfile

FROM python:3.11-slim

WORKDIR /app

# System dependencies for OCR and PDF
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy environment and install dependencies
COPY environment.yml .
RUN pip install --upgrade pip && pip install conda
RUN conda env create -f environment.yml || conda env update -f environment.yml

# Copy agent code
COPY src/backend ./backend

# Expose backend port
EXPOSE 8000

# Run backend
CMD ["conda", "run", "--no-capture-output", "-n", "agentic-legal-assistant", "uvicorn", "backend/app:app", "--host", "0.0.0.0", "--port", "8000"]