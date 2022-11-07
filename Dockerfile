FROM python:3.9.13-slim-buster

### Add requirements
ADD requirements.txt .

### Install pip requirements
RUN pip3 install -r requirements.txt && \
    rm -rf /var/lib/apt/lists/* /root/.cache /requirements.txt

### Set WORKDIR and pack code into images
WORKDIR /app
ADD . /app

CMD ["/bin/sh", "-c", "gunicorn --bind=0.0.0.0:80 --bind=0.0.0.0:8080 --timeout=300 --workers=2 --threads=8 --keep-alive=60 app:app"]
