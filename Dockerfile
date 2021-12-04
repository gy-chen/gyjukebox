FROM archlinux-yay

RUN sudo -u aur yay --noconfirm -S python-pyspotify
RUN pacman --noconfirm -S gstreamer gst-plugins-bad gst-plugins-good gst-plugins-ugly
RUN pacman --noconfirm -S python-pip gst-python uwsgi
WORKDIR /app
COPY . /app
RUN pip3 install .

CMD uwsgi --ini apps/app.ini
