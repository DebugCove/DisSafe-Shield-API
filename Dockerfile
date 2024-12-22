# Use the slim version of Python to reduce image size
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port for the application
EXPOSE 3000

# Set environment variables
ENV FLASK_ENV=production
ENV PORT_PRODUCTION=3000
ENV HOST=0.0.0.0

# Run the application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:3000", "run:app"]
