# Use a base Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy all project files
COPY . .

# Set PYTHONPATH to include /app/src
ENV PYTHONPATH="${PYTHONPATH}:/app/src"

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the FastAPI app
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
