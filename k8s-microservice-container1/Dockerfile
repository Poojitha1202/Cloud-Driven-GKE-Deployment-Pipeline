# Official Python runtime as a parent image
FROM python:latest

# Setting the working directory in the container
WORKDIR /app

# Copying the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Making port 6000 available to the world outside this container
EXPOSE 6000

# Running app.py when the container launches
CMD ["python", "container1.py"]
