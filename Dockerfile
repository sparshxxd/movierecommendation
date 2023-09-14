# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Install necessary development tools
RUN apt-get update && apt-get install -y gcc

# Set the working directory to /app
WORKDIR /recommender_App

# Copy the current directory contents into the container at /app
COPY . /recommender_App

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirement.txt

# Expose port 8501 for Streamlit app
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "homepage.py"]
