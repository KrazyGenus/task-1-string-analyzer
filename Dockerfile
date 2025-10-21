###########################################################################################
# Stage 1: The 'builder' stage is primarily for installing dependencies and tools.        #
###########################################################################################
FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/

WORKDIR /app

###########################################################################################
# CRITICAL CORRECTION POINT: Define the PYTHONPATH environment variable.                  #
# This tells the Python interpreter to include '/app' in the list of directories it       #
# searches for importable packages and modules (e.g., 'models').                          #
# Without this, Python often only searches the current working directory and system paths,#
# leading to the 'ModuleNotFoundError'.                                                 #
###########################################################################################
ENV PYTHONPATH=/app

COPY . /app

###########################################################################################
# Installs dependencies into a new virtual environment using 'uv sync'.                     #
###########################################################################################
RUN uv sync --frozen --no-cache

###########################################################################################
# Defines the PATH to ensure the uvicorn binary in the venv is executable via a short name.#
###########################################################################################
ENV PATH="/app/.venv/bin:$PATH"

###########################################################################################
# Specifies the default command to execute when the container starts.                       #
# Uvicorn correctly references the application 'app' within the 'main' module inside 'src'. #
###########################################################################################
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
