# Use an official Python runtime as a base image
FROM python:3.12-alpine

# Install system dependencies required by uv and your app
RUN apk add --no-cache curl git

# Install uv
RUN curl -LsSf -o /tmp/install_uv.sh https://astral.sh/uv/install.sh && \
    sh /tmp/install_uv.sh && \
    rm /tmp/install_uv.sh

# Make sure the uv binary is in the PATH
ENV PATH="/root/.local/bin:$PATH"

# Set the working directory in the container
WORKDIR /app

# Copy dependency files first for better Docker caching
COPY pyproject.toml uv.lock ./

# Install project dependencies using uv
RUN uv sync --frozen --no-dev --no-install-project

# Copy the rest of your application code
COPY . .

# Expose the port that your app will run on
EXPOSE 8000

# Command to run your application using Uvicorn
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
