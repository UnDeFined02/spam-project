# Use an official lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . /app/

# Expose port 8000 for the application
EXPOSE 8000

# Run the application using Gunicorn (better for production)
CMD ["gunicorn", "-b", "0.0.0.0:8000", "Spam_Project.wsgi:application"]
