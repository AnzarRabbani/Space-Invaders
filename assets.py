import pygame;pygame.init()

BLACK='#000000'
WHITE='#FFFFFF'
GREEN='#26FF1F'
RED='#FF1F26'

WIDTH,HEIGHT=800,800

WIN=pygame.display.set_mode((WIDTH,HEIGHT))

playerspeed=4
enemyspeed=5

laserspeed=6

playerhealth=5

playercooldown=250#ms
enemycooldown=500#ms

enemydirection=1

score=0

with open('highscore.txt','r') as f:
	highscore=int(f.read())

BACKGROUND=pygame.image.load('Assets/background.png').convert_alpha()
BACKGROUND=pygame.transform.scale(BACKGROUND,(WIDTH,HEIGHT))

PLAYER=pygame.image.load('Assets/player.png').convert_alpha()
PLAYER=pygame.transform.scale(PLAYER,(50,50))

ENEMY1=pygame.image.load('Assets/enemy1.png').convert_alpha()
ENEMY1=pygame.transform.scale(ENEMY1,(50,50))

ENEMY2=pygame.image.load('Assets/enemy2.png').convert_alpha()
ENEMY2=pygame.transform.scale(ENEMY2,(50,50))

ENEMY3=pygame.image.load('Assets/enemy3.png').convert_alpha()
ENEMY3=pygame.transform.scale(ENEMY3,(50,50))

ENEMY4=pygame.image.load('Assets/enemy4.png').convert_alpha()
ENEMY4=pygame.transform.scale(ENEMY4,(50,50))

LASER1=pygame.image.load('Assets/playerlaser.png').convert_alpha()
#LASER1=pygame.transform.scale(LASER1,(WIDTH,HEIGHT))

LASER2=pygame.image.load('Assets/enemylaser.png').convert_alpha()
#LASER2=pygame.transform.scale(LASER2,(WIDTH,HEIGHT))

class Ship:
	def __init__(self,x,y,img,speed,health,laserimg,laserspeed):
		self.img=img
		self.laserimg=laserimg
		self.rect=self.img.get_rect(center=(x,y))
		self.laser=self.laserimg.get_rect(center=(x,y))
		self.x=x
		self.y=y
		self.speed=speed
		self.health=health
		self.laserspeed=laserspeed
	def draw(self):
		WIN.blit(self.img,self.rect)
	def move(self,direction):
		self.rect.x+=self.speed*direction
	def movedown(self):
		self.rect.y+=1
	def shoot(self):
		WIN.blit(self.laserimg,self.laser)

class Laser:
	def __init__(self,x,y,img,speed):
		self.img=img
		self.rect=self.img.get_rect(center=(x,y))
		self.speed=speed
	def draw(self):
		WIN.blit(self.img,self.rect)
	def move(self):
		self.rect.y-=self.speed
