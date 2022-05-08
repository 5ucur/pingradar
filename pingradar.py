import sys
import time
import socket
import random
import threading
import subprocess

import math
from math import cos, sin

import pygame

def ping(ip):
	result = ''
	try:
		response = subprocess.check_output(
			['ping', '-c', '1', ip],
			stderr=subprocess.STDOUT,  # get all output
			universal_newlines=True  # return string not bytes
		)
		for word in response.split():
			if "time=" in word:
				result = word.strip("time=ms")
	except subprocess.CalledProcessError:
		result = 999999999999
	return int(float(result))


class PingManager:
	def __init__(self, ips):
		self.ips = ips
		self.info = {}

		for i, ip in enumerate(self.ips):
			#angle = i*34.88/100
			angle = i*(628/len(self.ips))/100
			self.info[ip] = {}
			self.info[ip]["angle"] = angle
			self.info[ip]["last_ms"] = 0

	def spawnThreads(self):
		for ip in self.ips:
			threading.Thread(target=self.pingThread, args=(ip,)).start()

	def pingThread(self, ip):
		result = ping(ip)
		self.info[ip]["last_ms"] = result

	def drawIps(self):
		for ip in self.info:
			angle = self.info[ip]["angle"]
			p_r = self.info[ip]["last_ms"]
			p_x = p_r * cos(angle) + CIRCLE_CENTER[0]
			p_y = p_r * sin(angle) + CIRCLE_CENTER[1]
			pygame.draw.circle(win, (0,255,0), (p_x, p_y), 5, 4)

			txt = font1.render(
				f"{ip} {self.info[ip]['last_ms']}ms",
				True,
				(0,255,0)
			)
			win.blit(txt, (p_x+5, p_y+5))

#svake 3 sekunde napraviti len(ips) threadova
#pa rezultat pisati u self.info[ip]["last_ms"]

pygame.init()
FPS = 60
clock = pygame.time.Clock()

pygame.font.init()
font1 = pygame.font.SysFont('Arial', 15)

WIDTH = 1024
HEIGHT = 768
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Radar")

CIRCLE_R = HALF_HEIGHT - 20 #radius
CIRCLE_CENTER = (HALF_WIDTH, HALF_HEIGHT) #x,y

angle = 0
toAdd = math.pi*2/FPS / 3 #3 seconds

ips = sys.argv[1:]
ping_manager = PingManager(ips)

ping_mngr_elapsed = 2500

running = True
while running:
	d = clock.tick(FPS)
	win.fill((0, 0, 0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	ping_mngr_elapsed += d

	if ping_mngr_elapsed > 3000: #3k ms == 3sec
		ping_manager.spawnThreads()
		ping_mngr_elapsed = 0

	ping_manager.drawIps()

	pygame.draw.circle(win, (0,255,0), CIRCLE_CENTER, CIRCLE_R, 1)
	pygame.draw.circle(win, (90,90,90), CIRCLE_CENTER, CIRCLE_R/3, 1)
	pygame.draw.circle(win, (90,90,90), CIRCLE_CENTER, CIRCLE_R/3*2, 1)

	p_r = CIRCLE_R
	p_x = p_r * cos(angle) + CIRCLE_CENTER[0]
	p_y = p_r * sin(angle) + CIRCLE_CENTER[1]
	pygame.draw.line(win, (0,255,0), CIRCLE_CENTER, (p_x, p_y), 1)


	pygame.draw.line(
		win,
		(127,127,127),
		(0, HALF_HEIGHT),
		(WIDTH, HALF_HEIGHT),
		1
	)

	pygame.draw.line(
		win,
		(127,127,127),
		(HALF_WIDTH, 0),
		(HALF_WIDTH, HEIGHT),
		1
	)

	pygame.display.update()
	angle += toAdd

pygame.quit()
quit()
