from pygame import *
from random import *
import time as tm
font.init()
font = font.Font(None, 36)
text = font.render("Счет: ", True, (255,255,255))

FPS = 120
win_width = 700
win_height= 500
window = display.set_mode((win_width,win_height))
display.set_caption("shooter")
clock = time.Clock()
# mixer.init()
# mixer.music.load('панк.ogg')
# mixer.music.play()
background = transform.scale( image.load('img/galaxy.jpg'),(700,500))
game_over = transform.scale( image.load('img/game-over.png'),(700,500))
thumb = transform.scale( image.load('img/thumb.jpg'),(700,500))

lost = 0
killed = 0
class GameSprite(sprite.Sprite):
	def __init__(self,player_image, player_x, player_y, player_speed):
		super().__init__()
		self.image = transform.scale( image.load(player_image) ,(65,65))
		self.speed = player_speed
		self.rect = self.image.get_rect()
		self.rect.x = player_x
		self.rect.y = player_y

	def reset(self):
		window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
	def __init__(self,player_image, player_x, player_y, player_speed):
		super().__init__(player_image, player_x, player_y, player_speed)
	def update(self):
		keys = key.get_pressed()
		if keys[K_RIGHT] and self.rect.x + 70 < win_width:
			self.rect.x += self.speed
		elif keys[K_LEFT] and self.rect.x>0:
			self.rect.x -= self.speed
	def fire(self):
		bullet = Bullet('img/bullet.png',self.rect.x, self.rect.y, 3)
		bullets.add(bullet)

class Enemy(GameSprite):
	def __init__(self,player_image, player_x, player_y, player_speed):
		super().__init__(player_image, player_x, player_y, player_speed)
	def update(self):
		global lost
		self.rect.y += self.speed
		if self.rect.y > win_height:
			lost += 1
			self.rect.x = randint(0, win_width-65)
			self.rect.y = 0

class Bullet(GameSprite):
	def __init__(self,player_image, player_x, player_y, player_speed):
		super().__init__(player_image, player_x, player_y, player_speed)
	def update(self):
		self.rect.y -= self.speed
		if self.rect.y < 0:
			self.kill()


bullets = sprite.Group()
player = Player("img/rocket.png",300,430,10)
kcas = sprite.Group()
for i in range(5): # количество появляемых енемис
	vrag = Enemy('img/ufo.png', randint(65, win_width-100),0,1)
	kcas.add(vrag)


game = True

while game:
	window.blit(background,(0,0))
	text = font.render("Счет: "+str(lost), True, (255,255,255))
	text2 = font.render("Убито: "+str(killed), True, (255,255,255))
	window.blit(text,(5,5))
	window.blit(text2,(5,30))
	player.reset()
	player.update()
	kcas.draw(window)
	kcas.update()
	bullets.draw(window)
	bullets.update()

	display.update()

	hits = sprite.groupcollide(bullets, kcas, True, True)
	for i in hits:
		killed += 1
		vrag = Enemy('img/ufo.png', randint(0, win_width-70),0,1)
		kcas.add(vrag)

	for i in event.get():
		if i.type == QUIT:
			game = False
		elif i.type == KEYDOWN:
			if i.key == K_SPACE:
				player.fire()
	if lost >= 10:
		# mixer.music.load('крик.ogg')
		# mixer.music.play()
		game = False
		window.blit(game_over,(0,0))
		display.update()
		tm.sleep(5)

	elif killed >= 30:
		game = False  
		window.blit(thumb,(0,0))
		display.update()
		tm.sleep(2)
	clock.tick(FPS)
