# Use the official Python 3.12 alpine image as the base image
FROM python:3.12-alpine

# Set the working directory inside the container All following commands will execute from /app
WORKDIR /app

# Copy only the requirements file first This improves Docker layer caching
COPY requirements.txt .

# Install all Python dependencies --no-cache-dir reduces the final image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the remaining application source code
COPY app/ .

# Document that the application listens on port 5000  (This does not publish the port)
EXPOSE 5000

#Start the Flask application when the container starts
CMD ["python3", "app.py"]
