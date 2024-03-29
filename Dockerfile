# Use an official Python runtime as the base image
FROM python:3.10.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt && rm -f requirements.txt

# Copy the application code to the container
COPY app/ /app/

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

CMD ["streamlit", "run", "graftool.py", "--server.port=8501", "--server.address=0.0.0.0", "--browser.gatherUsageStats=false"]