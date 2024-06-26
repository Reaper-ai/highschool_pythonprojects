import numpy as np
import pygame
from pygame.locals import *

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()
width, height = 700, 400
win = pygame.display.set_mode((width, height))

pygame.mixer.music.load('asset/sfx/theme.mp3')
jmp = pygame.mixer.Sound('asset/sfx/jump.wav')
die = pygame.mixer.Sound('asset/sfx/die.wav')
jmp.set_volume(0.2)
die.set_volume(0.5)
pygame.mixer.music.set_volume(0.5)

bgi = pygame.image.load('asset/img/bg.png').convert()
bg = pygame.transform.scale(bgi, (width, height))

gameover = False
i = 0
score = 0
p9, p135, p45,  p1 = 0.09, 0.135, 0.045, 0.1
y = -150

offset = [0, 20, -20, 40, -40, 50, -50, 80, -80, 100, -100]
probab = [p1, p135, p135, p9, p9, p9, p9, p9, p9, p45, p45]


class Bird(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()

		self.img = None
		self.x = x
		self.y = y
		self.w = 20
		self.h = 20
		self.vel = 0
		self.accn = 0.25
		self.spn = [pygame.image.load('asset/img/bird1.png').convert_alpha(),
					pygame.image.load('asset/img/bird2.png').convert_alpha()]
		self.spj = [pygame.image.load('asset/img/bird3.png').convert_alpha(),
					pygame.image.load('asset/img/bird4.png').convert_alpha()]

		self.spn[0] = pygame.transform.scale(self.spn[0], (60, 60))
		self.spn[1] = pygame.transform.scale(self.spn[1], (60, 60))
		self.spj[0] = pygame.transform.scale(self.spj[0], (60, 80))
		self.spj[1] = pygame.transform.scale(self.spj[1], (60, 80))

		self.cspn = 0
	def draw_bird(self):
		birdy = Rect(self.x, self.y, self.w, self.h)
		pygame.draw.rect(win, 'red', birdy)
		win.blit(self.img, (self.x - 10, self.y - 10))

	def update(self):
		if self.vel >= 0:
			if self.cspn < len(self.spn) - 1:
				self.cspn += 0.1
				self.img = self.spn[int(self.cspn)]
			else:
				self.cspn = 0
		elif 1 > self.vel > -3:
			self.img = self.spj[0]
		elif self.vel <= -3:
			self.img = self.spj[1]

	def gravity(self):
		if self.y < 380:
			self.vel += self.accn
			self.y += self.vel
		elif self.y > 381:
			loose(self)

	def jump(self):
		if self.y > 0:
			self.y += self.vel
		elif self.y <= 0:
			self.y = 0


class Wall(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()

		self.x = x
		self.y = y
		self.vel = 1
		self.h = 300
		self.w = 50

		self.img_u = pygame.image.load('asset/img/pipe_up.png').convert_alpha()
		self.img_d = pygame.image.load('asset/img/pipe_down.png').convert_alpha()
		self.img_u = pygame.transform.scale(self.img_u, (60, 300))
		self.img_d = pygame.transform.scale(self.img_d, (60, 300))

	def draw_wall(self):
		rect_up = (self.x, self.y, self.w, self.h)
		rect_down = (self.x, self.y + 450, self.w, self.h)

		pygame.draw.rect(win, 'green', rect_up)
		pygame.draw.rect(win, 'green', rect_down)

		rect_up = (self.x - 5, self.y, self.w, self.h)
		rect_down = (self.x - 5, self.y + 450, self.w, self.h)

		win.blit(self.img_u, rect_up)
		win.blit(self.img_d, rect_down)

	def move(self):
		global offset, probab
		self.x -= self.vel
		if self.x + 50 < 0:
			self.x = 700
			self.y = self.y + int(np.random.choice(offset, 1, p=probab))
			if self.y < -200:
				self.y = -200
			if self.y > 0:
				self.y = -200

	def collision(self, birdi):
		rect_bird = Rect(birdi.x, birdi.y, birdi.w, birdi.h)
		wall_up = Rect(self.x, self.y, self.w, self.h)
		wall_down = Rect(self.x, self.y + 450, self.w, self.h)

		col_wu = pygame.Rect.colliderect(rect_bird, wall_up)
		col_wd = pygame.Rect.colliderect(rect_bird, wall_down)

		if col_wd or col_wu:
			loose(birdi)

	def score(self, birdi):
		global score
		rect_bird = Rect(birdi.x, birdi.y, birdi.w, birdi.h)
		gap = Rect(self.x + 5, self.y + 350, 1, 100)
		if pygame.Rect.colliderect(rect_bird, gap):
			score += 5
			return score


bird = Bird(100, 100)

wall1 = Wall(400, -150)
wall2 = Wall(550, y + int(np.random.choice(offset, 1, p=probab)))
wall3 = Wall(700, y + int(np.random.choice(offset, 1, p=probab)))
wall4 = Wall(850, y + int(np.random.choice(offset, 1, p=probab)))
wall5 = Wall(1000, y + int(np.random.choice(offset, 1, p=probab)))

def draw_walls():
	wall1.draw_wall()
	wall2.draw_wall()
	wall3.draw_wall()
	wall4.draw_wall()
	wall5.draw_wall()

def move_walls():
	wall1.move()
	wall2.move()
	wall3.move()
	wall4.move()
	wall5.move()
def loose(birdi):
	wall1.vel = wall2.vel = wall3.vel = wall4.vel = wall5.vel = 0
	birdi.vel = birdi.accn = 0
	restart()


def restart():
	global gameover
	pygame.mixer.Sound.play(die, loops=0)
	pygame.mixer.music.stop()
	my_font = pygame.font.SysFont('Comic Sans MS', 72, 'b')
	text_surface = my_font.render("YOU LOSE", False, 'white')
	my_font = pygame.font.SysFont('Comic Sans MS', 24, 'b')
	tx = my_font.render("press enter to restart", False, 'white')
	s = pygame.Surface((700, 400), pygame.SRCALPHA)  # per-pixel alpha
	s.fill((66, 66, 245, 128))  # notice the alpha value in the color
	win.blit(s, (0, 0))
	win.blit(text_surface, (120, 100))
	win.blit(tx, (220, 200))
	gameover = True

def score_diplay(scor):
	scor = str(scor // 100)
	my_font = pygame.font.SysFont('Comic Sans MS', 30)
	text_surface = my_font.render(scor, False, 'white')
	win.blit(text_surface, (0, 0))

def scoring():
	wall1.score(bird)
	wall2.score(bird)
	wall3.score(bird)
	wall4.score(bird)
	wall5.score(bird)
def collide():
	wall1.collision(bird)
	wall2.collision(bird)
	wall3.collision(bird)
	wall4.collision(bird)
	wall5.collision(bird)

pygame.mixer.music.play(-1)
# Game loop.


while True:
	win.fill((0, 0, 0))
	win.blit(bg, (i, 0))
	win.blit(bg, (width + i, 0))
	i -= wall1.vel
	if i == -width:
		win.blit(bg, (width + i, 0))
		i = 0

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
		elif event.type == KEYDOWN:
			if event.key == pygame.K_SPACE:
				pygame.mixer.Sound.play(jmp)
				bird.vel = -4
				bird.jump()
		elif event.type == KEYUP:
			if event.key == pygame.K_SPACE:
				bird.jump()
			if event.key == pygame.K_RETURN and gameover:
				i = 0
				score = 0
				p9, p135, p45, p1 = 0.09, 0.135, 0.045, 0.1
				y = -150
				bird = Bird(100, 100)
				wall1 = Wall(400, -150)
				wall2 = Wall(550, y + int(np.random.choice(offset, 1, p=probab)))
				wall3 = Wall(700, y + int(np.random.choice(offset, 1, p=probab)))
				wall4 = Wall(850, y + int(np.random.choice(offset, 1, p=probab)))
				wall5 = Wall(1000, y + int(np.random.choice(offset, 1, p=probab)))
				pygame.mixer.music.play()
				gameover = False

	draw_walls()
	move_walls()
	bird.update()
	collide()
	bird.draw_bird()
	bird.gravity()
	scoring()
	score_diplay(score)
	pygame.display.flip()
	fpsClock.tick(fps)
