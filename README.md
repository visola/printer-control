# Printer Control

With the new Prusa MK4S I don't need Octoprint.
But I still want to have a camera and lights that I can control remotely.
This code contains a FastAPI server that is meant to run in a Raspberry PI (I'm using the RPi 4) and be exposed in your intranet.
It controls a LED strip with individually addresseable multicolor LEDs and assumes the strip has 30 of them.
It also assumes there's a camera installed in the RPi and will use that to display images from it.

## Initial Configuration

### SSH Login

To simplify logging in to the Raspberry Pi, setup a SSH key to be used, that way you don't have to type your password in every ssh or scp command.
TO do that, create an SSH private/public key pair using the following command:

```
$ ssh-keygen -t ed25519 -C "your_email@example.com"
```

It will ask where you want to store the key.
I stored it in the `~/.ssh` directory with a name that I'll remember what the key is for: `~/.ssh/printer_control_id_ed25519`.
I also use no password for the key so that I don't have to type anything when using it.

After that, you can install the key in the Raspberry Pi using the following command:

```
$ ssh-copy-id -i ${PATH_TO_PRIVATE_KEY} ${HOST}
```

It will ask for your SSH password and then never again.

### NeoPixels and sudo

I tried in many different ways to run the Neopixels library without sudo but wasn't able to.
If I use pin 19, I get the following message: `Gpio 19 is illegal for LED channel 0`
If I use pin 10, after enabling SPI, the pixels.py script runs but eventually all LEDs turn white and the script stop responding.

So instead of solving the sudo problem, I worked on making it work with Virtual Environments.
To do that you can ask sudo to preserve the venv in the context by adding: `-E env PATH=$PATH` to the sudo command, like this: `sudo -E env PATH=$PATH python3 pixels.py`
And then, it preserves the virtual environment and all works fine.

### Requirements

Install picamera2 using apt-get.
apt-get is the recommended way to ensure compatibility with libcamera and other libraries.
Run the following command:

```
$ sudo apt install -y python3-opencv
$ sudo apt install -y python3-picamera2 --no-install-recommends
```

Run the deploy script to copy the files into the Raspberry Pi:

```
$ scripts/deploy.sh
```

Then create a virtual enviroment and activate it:

```
$ python3 -m venv ${ENV_NAME}
$ source ${EVN_NAME}/bin/activate
```

Install all dependencies using the requirements.txt file:

```
$ pip install -r requirements.txt
```

### Backend

Using FastAPI and Uvicorn you can quickly create a HTTP server with an easy to maintain API and also serve static files.

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
