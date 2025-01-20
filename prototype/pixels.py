import time
import board
import neopixel
import signal
import sys

pixel_pin = board.D18
num_pixels = 30

ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1.0, pixel_order=ORDER, auto_write=False)

def signal_handler(sig, frame):
	pixels.fill((0, 0, 0))
	pixels.show()
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def wheel(pos):
	if pos < 0 or pos > 255:
		r = g = b = 0
	elif pos < 85:
		r = int(pos * 3)
		g = int(255 - pos * 3)
		b = 0
	elif pos < 170:
		pos -= 85
		r = int(255 - pos * 3)
		g = 0
		b = int(pos * 3)
	else:
		pos -= 170
		r = 0
		g = int(pos * 3)
		b = int(255 - pos * 3)
	return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)

def rainbow_cycle(wait):
	for j in range(255):
		for i in range(num_pixels):
			pixel_index = (i * 256 // num_pixels) + j
			pixels[i] = wheel(pixel_index & 255)
			pixels.show()
			time.sleep(wait)

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

while True:
	in_to_out((255, 255, 255), 0.05)
	time.sleep(0.5)
	out_to_in((0, 0, 0), 0.05)
	time.sleep(0.5)

	for color in [ (255, 0 , 0), (0, 255, 0), (0, 0, 255) ]:
		in_to_out(color, 0.01)
		time.sleep(0.5)
		out_to_in((0, 0, 0), 0.01)
		time.sleep(0.5)

	rainbow_cycle(0.001)
	rainbow_cycle(0.001)