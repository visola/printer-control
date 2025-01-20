# Printer Control

With the new Prusa MK4S I don't need Octoprint.
But I still want to have a camera and lights that I can control remotely.
This code contains a FastAPI server that is meant to run in a Raspberry PI (I'm using the RPi 4) and be exposed in your intranet.
It controls a LED strip with individually addresseable multicolor LEDs and assumes the strip has 30 of them.
It also assumes there's a camera installed in the RPi and will use that to display images from it.

### Requirements

For the neopixel controller, I got this from [this article](https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage):

```
sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel
sudo python3 -m pip install --force-reinstall adafruit-blinka
```

### Backend

Using FastAPI and Uvicorn you can quickly create a HTTP server with an easy to maintain API and also serve static files.

To initiate your virtual environment and install dependencies:

```
python3 -m venv ./venv
source ./venv/bin/activate
```

To start the server locally use:

```
uvicorn main:app --reload --host 0.0.0.0
```

### Frontend

Uses Vite and React.
Source code is in `./frontend`.
Publishes the assets to the `./public` so that it can be served statically from FastAPI.

To develop locally, run:

```
npm run watch
```

This will publish the files the root `public` folder and updates will be picked up by the FastAPI server.

### Deployment

To deploy the files to the Raspberry Pi, you can run the script `scripts/deploy.sh`.
This script depends on two variables:

- $SSH_OPTIONS = options to be passed to ssh and scp used to copy files to the RPi, I used `-i /path/to/private_key`
- $HOST = hostname for your Raspberry Pi

To make sure the server starts after booting up, I added a Systemd configuration file.
Make sure to update the `printer_control.service` file since it has the path to the start script hardcoded.
To install this configuration file, you need to copy it over to the `/lib/systemd/system` and then enable it with the following commands:

```
$ sudo systemctl daemon-reload
$ sudo systemctl enable printer_control.service
```

After the next boot, it should start the server.
