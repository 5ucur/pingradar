import sys
import time
import socket
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
	except subprocess.CalledProcessError:
	    response = None
	for word in response.split():
		if "time=" in word:
			result = word.strip("time=ms")
	return int(result)

class PingManager:
	def __init__(self, ips):
		self.ips = ips
		self.threads = []

ips = sys.argv[1:]

pygame.init()
FPS = 60
clock = pygame.time.Clock()

WIDTH = 640
HEIGHT = 480
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Radar")

CIRCLE_R = HALF_HEIGHT - 20 #radius
CIRCLE_CENTER = (HALF_WIDTH, HALF_HEIGHT) #x,y

tick = 0
angle = 0
toAdd = math.pi/2 / FPS #3 seconds

running = True
while running:
	clock.tick(FPS)
	win.fill((0, 0, 0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	pygame.draw.circle(win, (0,255,0), CIRCLE_CENTER, CIRCLE_R, 1)
	pygame.draw.circle(win, (0,255,0), CIRCLE_CENTER, 5, 5)

	p_r = CIRCLE_R #test radius
	p_x = p_r * cos(angle) + CIRCLE_CENTER[0]
	p_y = p_r * sin(angle) + CIRCLE_CENTER[1]
	#pygame.draw.circle(win, (255,0,0), (p_x, p_y), 5, 5)
	pygame.draw.line(win, (0,255,0), CIRCLE_CENTER, (p_x, p_y), 1)

	pygame.display.update()
	tick += 1
	angle += toAdd

pygame.quit()
quit()
