import warnings
warnings.filterwarnings('ignore',category=RuntimeWarning)

import pygame;pygame.init();pygame.font.init()
import random
from assets import *

pygame.display.set_caption('Space Invaders')
clock=pygame.time.Clock()
FONT1=pygame.font.SysFont('Comic Sans MS',30)
FONT3=pygame.font.SysFont('Comic Sans MS',50)
FONT2=pygame.font.SysFont('Comic Sans MS',100)

player=Ship(WIDTH/2,700,PLAYER,playerspeed,playerhealth,LASER1,laserspeed)

playerlasers=[]
lastshottime=0

enemylist=[]
enemylasers=[]

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



padding=30
spacing=ENEMY1.get_width()+padding
enemiesdead=True

decending=False
decendingLeft=0

def enemygroupsize():
	groupsize=random.randint(1,8)
	return groupsize

def draw_enemies():
	global enemiesdead;enemiesdead=False
	global design;design=enemydesign()
	global groupsize;groupsize=enemygroupsize()
	for x in range(int((WIDTH/spacing)-2)):
		for y in range(groupsize):
			enemylist.append(Ship((x*spacing)+50,(y*-80)-40,design,enemyspeed,1,LASER2,laserspeed))

GameOverText=FONT2.render('Game Over',False,WHITE)
RestartText=FONT3.render('Press r to restart or q to quit',False,WHITE)

state='playing'

run=True
while run:

	if state=='playing':
		clock.tick(60)
		WIN.fill(BLACK)
		WIN.blit(BACKGROUND,(0,0))

		scoreText=FONT1.render('Score: '+str(score),False,WHITE)
		highscoreText=FONT1.render('Highscore: '+str(highscore),False,WHITE)

		WIN.blit(scoreText,(20,750))
		WIN.blit(highscoreText,(20,770))

		player.draw()

		greenHealthRect=pygame.Rect(player.rect.x,player.rect.y+player.rect.height,playerhealth*10,10)
		redHealthRect=pygame.Rect(player.rect.x+greenHealthRect.width,player.rect.y+player.rect.height,(5-playerhealth)*10,10)
		pygame.draw.rect(WIN,GREEN,greenHealthRect)
		pygame.draw.rect(WIN,RED,redHealthRect)

		if enemiesdead:
			draw_enemies()
			print(groupsize)
		
		if len(enemylist)==0:
			enemiesdead=True
			score+=50

		for enemy in enemylist:
			enemy.draw()

		hitedge=False
		for enemy in enemylist:
			if enemy.rect.center[0]<=40 or enemy.rect.center[0]>=WIDTH-40:
				hitedge=True
				break
		
		if hitedge:
			enemydirection*=-1
			decending=True
			decendingLeft=40

		if decending:
			decendingLeft-=1
			for enemy in enemylist:
				enemy.movedown()
			if decendingLeft<=0:
				decending=False

		for enemy in enemylist:
			enemy.move(enemydirection)

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
		
		shot_enemy=None
		laser_shot=None
		for laser in playerlasers:
			for enemy in enemylist:
				if laser.rect.colliderect(enemy):
					shot_enemy=enemy
					laser_shot=laser
					score+=10
					break
		
		playershot=None
		for laser in enemylasers:
			if laser.rect.colliderect(player.rect):
				playershot=laser
				break

		playertouch=False
		for enemy in enemylist:
			if enemy.rect.center[1]+(1.5*ENEMY1.get_height())>=player.rect.y+player.rect.height:
				playertouch=True
				break
		
		if playertouch:
			playerhealth=0

		if playershot:
			enemylasers.remove(playershot)
			playerhealth-=1
			print(playerhealth)

		if playerhealth<=0:
			if score>highscore:
				highscore=score
				with open('highscore.txt','w') as f:
					f.write(str(score))
			state='gameover'

		if shot_enemy:
			enemylist.remove(shot_enemy)
			playerlasers.remove(laser_shot)

		def willEnemyshoot():
			number=random.randint(1,1000)
			if number==1:
				return True

		for enemy in enemylist:
			if willEnemyshoot():
				enemylasers.append(Laser(enemy.rect.center[0],enemy.rect.center[1],LASER2,laserspeed*-1))
		
		for laser in enemylasers:
			laser.draw()
			laser.move()

		keys=pygame.key.get_pressed()
		if keys[pygame.K_LEFT] and player.rect.center[0]>=(player.rect.width/2):
			player.move(-1)
		if keys[pygame.K_RIGHT] and player.rect.center[0]<=(WIDTH-(player.rect.width/2)):
			player.move(1)

		pygame.display.update()
	
	elif state=='gameover':
		clock.tick(60)
		WIN.blit(GameOverText,((WIDTH/2)-(GameOverText.get_width()/2),(HEIGHT/2)-(GameOverText.get_height()/2)))
		WIN.blit(RestartText,((WIDTH/2)-(RestartText.get_width()/2),(HEIGHT/2)-(RestartText.get_height()/2)+50))

		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				run=False

			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_q:
					run=False
				if event.key==pygame.K_r:
					score=-50
					playerhealth=5
					state='playing'
					enemylist=[]
					playerlasers=[]
					enemylasers=[]
		pygame.display.update()
		

pygame.quit()
