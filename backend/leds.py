import board
import neopixel
import time
from pydantic import BaseModel

pixel_pin = board.D18
num_pixels = 30
half_pixels = int(num_pixels / 2)

ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.1, pixel_order=ORDER, auto_write=False)

class LedState(BaseModel):
	on: bool

led_state = LedState(on=False)

def in_to_out(color, interval):
	for i in range(0, num_pixels):
		pixels[i] = color
		pixels.show()
		time.sleep(interval)

def out_to_in(color, interval):
	for i in range(num_pixels - 1, -1, -1):
		pixels[i] = color
		pixels.show()
		time.sleep(interval)

def split_from_middle(color, interval):
	for i in range(half_pixels - 1, -1, -1):
		pixels[i] = color
		pixels[num_pixels - i - 1] = color
		pixels.show()
		time.sleep(interval)

def join_in_middle(color, interval):
	for i in range(0, half_pixels):
		pixels[i] = color
		pixels[num_pixels - i - 1] = color
		pixels.show()
		time.sleep(interval)

def toggle_leds(new_state: LedState):
	global led_state
	
	if new_state.on:
		in_to_out((255, 255, 255), 0.01)
		led_state.on = True
		return led_state

	out_to_in((0, 0, 0), 0.01)
	led_state.on = False
	return led_state

def get_leds_state():
	return led_state

def register_endpoints(app):
	app.router.add_api_route("/leds", toggle_leds, methods=["PUT"])
	app.router.add_api_route("/leds", get_leds_state, methods=["GET"])

def shutdown_hook():
	join_in_middle((0, 0, 0), 0.02)
