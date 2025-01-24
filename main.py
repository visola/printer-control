from backend import camera, leds 
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import signal

app = FastAPI()

app_api = FastAPI()

app.mount("/api", app_api)
app.mount("/", StaticFiles(directory="public", html=True), name="public")

leds.join_in_middle((255, 255, 0), 0.05)
leds.split_from_middle((0, 255, 0), 0.05)
leds.join_in_middle((255, 255, 255), 0.05)
leds.split_from_middle((0, 0, 0), 0.05)

leds.register_endpoints(app_api)
camera.register_endpoints(app_api)

def signal_handler(sig, frame):
	leds.shutdown_hook()
	camera.shutdown_hook()
	print('Good bye!')

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
