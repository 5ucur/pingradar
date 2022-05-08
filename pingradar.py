import pygame

pygame.init()

FPS = 60
clock = pygame.time.Clock()

WIDTH = 1270
HEIGHT = 720
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Radar")

running = True
while running:
	clock.tick(FPS)
	win.fill((0, 0, 0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	#game code

	pygame.display.update()

pygame.quit()
quit()