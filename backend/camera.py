# This backend needs picamera2 and opencv to install, run the following command:
# sudo apt install python3-opencv python3-picamera2

from fastapi.responses import StreamingResponse
from picamera2 import Picamera2
from libcamera import controls
import cv2
import io

camera = Picamera2()
camera.options["quality"] = 95
camera.options["compress_level"] = 2

config = camera.create_preview_configuration(main={"size": (1920, 1080)})
camera.align_configuration(config)
print(config)
camera.configure(config)
camera.start()

should_stop = False

def generate_frames():
	def image_stream():
		while True:
			if should_stop:
				return

			frame = camera.capture_array("main")
			ret, buffer = cv2.imencode('.jpg', frame)
			frame = buffer.tobytes()
			yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

	return StreamingResponse(image_stream(), media_type="multipart/x-mixed-replace; boundary=frame")

def register_endpoints(app):
	app.router.add_api_route("/camera", generate_frames, methods=["GET"])

def shutdown_hook():
	global should_stop
	should_stop = True
