# Using base template.
FROM python:3.11-slim

WORKDIR /app

# Copy project.
COPY . /app/

# Downloading requirements
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x start.sh

# Launch.
CMD ["./start.sh"]
