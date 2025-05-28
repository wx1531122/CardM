# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# --no-cache-dir: Disables the pip cache, which can reduce image size.
# -r requirements.txt: Specifies the requirements file.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
# This includes app.py, models.py, and the directories: database, static, templates
COPY . .
# Note: The above COPY command assumes the Dockerfile is in card_scheduler_project
# and the build context is card_scheduler_project.
# If the build context is the parent directory, then the COPY commands would be:
# COPY card_scheduler_project/requirements.txt .
# COPY card_scheduler_project/ .

# Run models.py to initialize the database and create the tables
# This ensures the database directory and schedule.db file (with tables) are present in the image.
RUN python models.py

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variables (optional, but good practice for Flask)
# ENV FLASK_APP app.py # No longer needed as we use CMD ["python", "app.py"]
# ENV FLASK_RUN_HOST 0.0.0.0 # This is handled in app.py's app.run()

# Run app.py when the container launches
# The app.py is already configured to run on host 0.0.0.0 and port 5000
CMD ["python", "app.py"]
