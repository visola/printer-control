from backend import camera, leds 
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import signal

app = FastAPI()

app_api = FastAPI()

app.mount("/api", app_api)
app.mount("/", StaticFiles(directory="public", html=True), name="public")

camera.register_endpoints(app_api)
leds.register_endpoints(app_api)

def signal_handler(sig, frame):
	leds.shutdown_hook()
	camera.shutdown_hook()
	print('Good bye!')

signal.signal(signal.SIGINT, signal_handler)
