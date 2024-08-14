# Use the official Python base image
FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m playwright install

# Copy the content of the local src directory to the working directory
COPY . .

# Command to run the application
CMD ["python", "main.py"]
