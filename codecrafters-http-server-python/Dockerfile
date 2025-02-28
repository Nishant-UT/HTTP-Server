# Use official Python image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install dependencies (if using pipenv, change this line)
RUN pip install -r requirements.txt

# Expose the new port
EXPOSE 9999

# Define the command to run your server
CMD ["python", "app/main.py"]
