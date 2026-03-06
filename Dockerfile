# Use an official Python runtime as a parent image
FROM python:3.11-slim


# Prevent python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*
    
# Install poetry
RUN pip install poetry


# Disable Poetry virtual environments
RUN poetry config virtualenvs.create false

# Copy Poetry files
COPY pyproject.toml poetry.lock /app/

# Install dependencies
RUN poetry install --no-root

# Copy the current directory contents into the container at /app
COPY . .

RUN chmod +x start.sh



# Make port 8000 available to the world outside this container
EXPOSE 8000

# # Run app.py when the container launches

CMD ["./start.sh"]