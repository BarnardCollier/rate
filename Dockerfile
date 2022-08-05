FROM python:3.8.13-slim-buster
LABEL Maintainer="jacques@desroches.ca"

WORKDIR /usr/app/src

RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install cron
#RUN apt-get update && apt-get -y install cron

COPY . .

CMD ["python3","./main.py"]
