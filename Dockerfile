# Use the official Python image as the base image
FROM python:3.8

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000

# Define environment variable for Flask to run in production mode
ENV FLASK_ENV=production

# Command to run the application
CMD ["python", "app.py"]
