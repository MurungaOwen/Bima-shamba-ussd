# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy requirements if available, else fallback to install FastAPI and Uvicorn
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt || pip install --no-cache-dir fastapi uvicorn

# Copy the rest of the application code
COPY . .

# Expose the port FastAPI will run on
EXPOSE 3000

# Command to run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
