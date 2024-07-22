# Official Python runtime as a parent image
FROM python:latest

# Setting the working directory in the container
WORKDIR /app

# Copying the Flask application's requirements
COPY requirements.txt ./

# Installing any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copying the rest of the application's source code from our host to the image filesystem.
COPY container2.py .

# Define the directory to mount the host volume
VOLUME [ "/data" ]

# Expose the port the app runs on
EXPOSE 4000

# Run app.py when the container launches
CMD ["python", "container2.py"]