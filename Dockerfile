# FROM python:3.9-slim

# # Set working directory
# WORKDIR /app

# # Copy application files and model artifacts
# COPY flask_app/ /app/
# COPY artifacts/data/vectorized/vectorizer.pkl /app/artifacts/data/vectorized/vectorizer.pkl
# COPY flask_app/requirements.txt /app/

# # Install dependencies and clean up cache in a single layer
# RUN pip install --no-cache-dir -r requirements.txt && \
#     rm -rf /root/.cache/pip

# # Expose port
# EXPOSE 5000

# # Run application using Gunicorn (production-ready WSGI server)
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]


# -------------------------- multi stage build below to reduce size -----------------


# Stage 1: Builder
FROM python:3.10-slim AS build

WORKDIR /app

# Copy only requirements first (Docker layer caching)
COPY flask_app/requirements.txt .

# Install dependencies
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Final minimal runtime image
FROM python:3.10-slim AS final

WORKDIR /app

# Copy installed python packages from build stage
COPY --from=build /root/.local /root/.local

# Set PATH so installed packages (gunicorn) are found
ENV PATH=/root/.local/bin:$PATH

# Copy app code and artifacts
COPY flask_app/ /app/
COPY artifacts/data/vectorized/vectorizer.pkl /app/artifacts/data/vectorized/vectorizer.pkl

# Expose app port
EXPOSE 5000

# Run with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
