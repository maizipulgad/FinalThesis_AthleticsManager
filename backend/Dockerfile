# Use the official Python image as a base image
FROM python:3.9.13

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend project into the container
COPY . .

# Set environment variables for Django
ENV DJANGO_SETTINGS_MODULE=FinalThesis_AthleticsManager.settings
ENV PYTHONUNBUFFERED=1

# Expose the port
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]