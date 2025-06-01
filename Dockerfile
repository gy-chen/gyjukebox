FROM archlinux

RUN pacman --noconfirm -Sy gstreamer gst-plugins-bad gst-plugins-good gst-plugins-ugly
RUN pacman --noconfirm -Sy python-pip gst-python uwsgi uwsgi-plugin-python
WORKDIR /app
COPY . /app
RUN pip3 install --break-system-packages .

CMD uwsgi --ini apps/app.ini
