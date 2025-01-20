from picamzero import Camera
import time

print('Initializing...')
camera = Camera()
camera.flip_camera(vflip=True, hflip=True)
camera.resolution = (1024, 768)

for i in range(0, 3):
	print(f'Taking picture...')
	now = time.time()
	camera.take_photo(f'foo-{i}.jpg')
	print(f'Done in {time.time() - now}s')
