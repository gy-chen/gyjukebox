FROM archlinux-yay

RUN sudo -u aur yay --noconfirm -S python-pyspotify
RUN pacman --noconfirm -Sy gstreamer gst-plugins-bad gst-plugins-good gst-plugins-ugly
RUN pacman --noconfirm -Sy python-pip gst-python uwsgi uwsgi-plugin-python
WORKDIR /app
COPY . /app
RUN pip3 install .

CMD uwsgi --ini apps/app.ini
