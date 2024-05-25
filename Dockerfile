# Use the official Python 3.12 image from the Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY const.py /app/
COPY api/ /app/api/
COPY data/ /app/data/
COPY main.py /app/
COPY main_pipelines.py /app

# Command to run the application
ENTRYPOINT ["sh", "-c", "python main_pipelines.py && python main.py"]
