FROM python:3.13-slim

# Install Git 
RUN apt-get update && apt-get install -y git 

# Create non-root user
RUN useradd -m botuser

# Set environment variables
ENV DAGSTER_HOME=/app/dagster_home

# Create necessary directories
RUN mkdir -p /app /data $DAGSTER_HOME /home/botuser/.dbt \
    && chown -R botuser:botuser /app /data $DAGSTER_HOME /home/botuser/.dbt

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY . .

# Fix permissions
RUN chown -R botuser:botuser /app

# Make script executable
RUN chmod +x entrypoint.sh

# Switch to non-root
USER botuser

CMD ["./entrypoint.sh"]