# Use the official Python 3.12 image from the Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application code into the container
COPY const.py /app/
COPY api/ /app/api/
COPY data/ /app/data/
COPY main.py /app/
COPY main_pipelines.py /app/
COPY requirements.txt /app/

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the entrypoint to run the application
ENTRYPOINT ["sh", "-c", "sleep 20 && uvicorn main:app --host 0.0.0.0 --port 8000"]
