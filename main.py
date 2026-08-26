import warnings
warnings.filterwarnings('ignore',category=RuntimeWarning)

import pygame;pygame.init();pygame.font.init()
import random
from assets import *

pygame.display.set_caption('Space Invaders')
clock=pygame.time.Clock()

player=Ship(WIDTH/2,700,PLAYER,playerspeed,playerhealth,LASER1,laserspeed)

playerlasers=[]
lastshottime=0

enemylist=[]

def enemygroupsize():
	groupsize=random.randint(1,10)
	return groupsize

groupsize=1

def enemydesign():
	number=random.randint(1,4)
	if number==1:
		design=ENEMY1
	elif number==2:
		design=ENEMY2
	elif number==3:
		design=ENEMY3
	elif number==4:
		design=ENEMY4
	return design

design=enemydesign()

padding=30
spacing=ENEMY1.get_width()+padding

for x in range(int(WIDTH/spacing)):
	for y in range(groupsize):
		enemylist.append(Ship((x*spacing)+40,(y*50)+50,design,enemyspeed,1,LASER2,laserspeed))

run=True
while run:
	clock.tick(60)
	WIN.fill(BLACK)
	WIN.blit(BACKGROUND,(0,0))

	player.draw()
			
	for enemy in enemylist:
		enemy.draw()

	for enemy in enemylist:
		if enemy.rect.center[0]<=40:
			enemydirection*=-1
			enemy.movedown()
			break
		elif enemy.rect.center[0]>=WIDTH-40:
			enemydirection*=-1
			enemy.movedown()
			break
	
	for enemy in enemylist:
		enemy.move()

	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			run=False
		if event.type==pygame.KEYDOWN:
			if event.key==pygame.K_q:
				run=False
			if event.key==pygame.K_SPACE:	
				if (pygame.time.get_ticks()-lastshottime)>playercooldown:
					playerlasers.append(Laser(player.rect.center[0],player.rect.center[1],LASER1,laserspeed))
					lastshottime=pygame.time.get_ticks()
				
	for laser in playerlasers:
		laser.draw()
		laser.move()


	keys=pygame.key.get_pressed()
	if keys[pygame.K_LEFT]:
		player.moveleft()
	if keys[pygame.K_RIGHT]:
		player.moveright()

	pygame.display.update()

pygame.quit()
