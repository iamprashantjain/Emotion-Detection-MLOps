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


# stage1: builder stage
FROM python:3.10 AS build

WORKDIR /app

# Copy application files and model artifacts
COPY flask_app/ /app/
COPY artifacts/data/vectorized/vectorizer.pkl /app/artifacts/data/vectorized/vectorizer.pkl
COPY flask_app/requirements.txt /app/

# Install dependencies and clean up cache in a single layer
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip

#stage2: final stage
FROM python:3.10 AS final

WORKDIR /app

#copy only necessary files form build stage
COPY --from=build /app /app

#expose app port
EXPOSE 5000

# Run application using Gunicorn (production-ready WSGI server)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
