# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the pyproject.toml and uv.lock files to the container
COPY pyproject.toml uv.lock ./

# Install Poetry for dependency management
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-dev

# Copy the source code to the container
COPY src/ ./src

# Expose the port the app runs on
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]