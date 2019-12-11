FROM ubuntu:19.04

RUN apt-get update
RUN apt-get install -y wget gnupg
RUN wget -q -O - https://apt.mopidy.com/mopidy.gpg | apt-key add -
RUN wget -q -O /etc/apt/sources.list.d/mopidy.list https://apt.mopidy.com/buster.list
RUN apt-get update
RUN apt-get install -y libspotify-dev
RUN apt-get install -y build-essential python3-dev libffi-dev
RUN apt-get install -y python3-gst-1.0 \
    gir1.2-gstreamer-1.0 gir1.2-gst-plugins-base-1.0 \
    gstreamer1.0-plugins-good gstreamer1.0-plugins-ugly \
    gstreamer1.0-tools gstreamer1.0-plugins-bad
RUN apt-get install -y python3-pip
WORKDIR /app
COPY . /app
RUN pip3 install .

CMD uwsgi --ini apps/app.ini
