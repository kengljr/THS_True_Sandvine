# Add Python 3.8 to the image
FROM python:3.11

RUN  apt-get update \
  && apt-get install -y wget unzip nano chromium-chromedriver

  # install chrome directly
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

# install chromedriver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

WORKDIR /app

# Copy the requirements.txt file to /app
COPY requirements.txt /app/requirements.txt

# Install Python dependencies listed in requirements.txt
RUN pip install -r /app/requirements.txt

# Copy the Python script 'app.py' to /app
COPY . /app/

# Declare a volume at the specified path for persistent data storage
# VOLUME /home/dugdic/sandvine
VOLUME /Users/kengljr/Project/monitoring_provisioner
# (eg:-VOLUME /media/projects/Test)

