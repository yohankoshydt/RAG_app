# Use an official Python image as a base (choose the Python version you need)
FROM python:3.10-slim

# Set environment variables to avoid interactive prompts during installation
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive

# Set up a working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the entire project into the container
COPY . /app

# Expose a port if your app needs it (for example, Streamlit apps use 8501)
EXPOSE 8501

# Define the default command to run your app (update this based on your entry file)
CMD ["streamlit run", "app.py" ]
