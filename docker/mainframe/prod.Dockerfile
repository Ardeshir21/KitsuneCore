# Dockerfile.prod

# Use a specific Python version
FROM python:3.6.9

# Set the working directory
WORKDIR /app/nine-tails


# Copy all the application files into the container
COPY ./ ./

# Upgrade pip to the latest version
RUN pip install --no-cache-dir --upgrade pip

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that the app will run on
EXPOSE 9000

# Command to run the application (can be overridden in docker-compose.yml)
CMD ["gunicorn", "KitsuneCore.wsgi:application", "--bind", "0.0.0.0:9000"]

