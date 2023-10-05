FROM python:3.9-slim-buster

WORKDIR /flask

RUN apt-get update && apt-get install -y \
    default-jre \
    build-essential \
    libssl-dev \
    gcc \
    libffi-dev \
    python3-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set the FLASK_APP environment variable
ENV FLASK_APP=app.py

# Expose port 5000 for the Flask application to listen on
EXPOSE 7001

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=7001"]
#CMD ["flask", "run"]
