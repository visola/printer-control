import board
import neopixel
import time
from pydantic import BaseModel

pixel_pin = board.D18
num_pixels = 30

ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1.0, pixel_order=ORDER, auto_write=False)

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

def toggle_leds(new_state: LedState):
	global led_state
	
	if new_state.on:
		in_to_out((255, 255, 255), 0.01)
		led_state.on = True
		return led_state

	out_to_in((0, 0, 0), 0.01)
	led_state.on = False
	return led_state

def register_endpoints(app):
	app.router.add_api_route("/leds", toggle_leds, methods=["PUT"])

def shutdown_hook():
	pixels.fill((0, 0, 0))
	pixels.show()
