# backend/Dockerfile

# Stage 1: Use an official Python runtime as a parent image
# Using a specific version is a good practice for reproducibility.
FROM python:3.10-slim

# Stage 2: Set the working directory inside the container
# All subsequent commands will be run from this path.
WORKDIR /app

# Stage 3: Copy the dependencies file and install them
# We copy only requirements.txt first to leverage Docker's layer caching.
# If this file doesn't change, Docker won't re-run the pip install step, speeding up builds.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 4: Copy the rest of the application code into the container
COPY . .

# Stage 5: Expose the port the app runs on
# This tells Docker that the container listens on port 5001.
EXPOSE 5001

# Stage 6: Define the command to run the application
# This is what starts our Flask server when the container launches.
CMD ["python", "app.py"]
