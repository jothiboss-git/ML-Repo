# Use a minimal Python 3.9 base image
FROM python:3.9-slim-bookworm

# Install necessary dependencies
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download and install `uv`
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure `uv` is available in PATH
ENV PATH="/root/.local/bin/:$PATH"

# Set the working directory inside the container
WORKDIR /app

# Copy the project into the image
ADD . /app

# Create a virtual environment before running `uv sync`
RUN python -m venv /app/.venv && \
    . /app/.venv/bin/activate && \
    uv sync --frozen

# Ensure the virtual environment is activated when running commands
ENV PATH="/app/.venv/bin:$PATH"

# Run the application
CMD ["uv", "run", "run.py"]
