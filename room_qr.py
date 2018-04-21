import pyqrcode
import png
import os


rooms = list(map(lambda a: a.split('.')[0], os.listdir('./rooms')))
for room in rooms:
	url = pyqrcode.create(f'https://evanmackay.ca/Full-Calendar/FullCalendar.html?room={room}')
	url.png(f'qrcodes/{room}.png', scale=6, module_color=[0, 0, 0, 128], background=[255,255,255])