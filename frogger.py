import sys, pygame, random
from pygame.locals import *

pygame.init()
screen_height = 750
screen_width = 1200
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Frogger")
FPS = 200
screen_rect = screen.get_rect()

player = pygame.image.load('frog.bmp')
player_rect = player.get_rect()
player_rect.left = 300 + 11
player_rect.top = screen_height - 68

logs = []
logs.append(pygame.image.load('1x1_log.bmp'))
logs.append(pygame.image.load('2x1_log.bmp'))
logs.append(pygame.image.load('3x1_log.bmp'))

cars = []
cars.append(pygame.image.load('1x1_car.bmp')) #RIGHT
cars.append(pygame.image.load('2x1_car.bmp')) #LEFT
cars.append(pygame.image.load('3x1_car.bmp')) #LEFT

not_in_ocean = False

level = 1
gameover = False

#For player movement
up_movements = 0
down_movements = 0
left_movements = 0 
right_movements = 0
up_movement = False
down_movement = False
left_movement = False
right_movement = False

x_logs = [0, 600]
ys = [74, 149, 224, 299, 374, 449, 524, 599] 
widths = [1, 2, 3]
log_height = 74
logs_created = []
speeds = []
speeds1 = []
speeds3 = []
speeds5 = []
speeds7 = []
speeds9 = []
for y in ys:
	speeds.append(random.randint(1,3))
	speeds1.append(random.randint(1,3))
	speeds3.append(random.randint(2,3))
	speeds5.append(random.randint(2,4))
	speeds7.append(random.randint(2,5))
	speeds9.append(random.randint(3,5))



cars_created = []

order = 0
choice_1 =''

start = True

orders = [2, 6, 3, 5, 4]
choice = ['river', 'street']
street_choice = False
river_choice = False

FONT = pygame.font.Font('freesansbold.ttf', 32)
BIG_FONT = pygame.font.Font('freesansbold.ttf', 144)



gameover_text = BIG_FONT.render('GAME OVER', True, (255, 0, 0))
gameover_text_rect = gameover_text.get_rect()
gameover_text_rect.centerx = screen_rect.centerx
gameover_text_rect.centery = screen_rect.centery

restart_text = FONT.render('Hit R to Play Again', True, (255, 255, 255))
restart_text_rect = restart_text.get_rect()
restart_text_rect.top = gameover_text_rect.bottom
restart_text_rect.centerx = screen_rect.centerx

score_text = FONT.render('Level: ' + str(level), True, (0,0,0))
score_text_rect = score_text.get_rect()
score_text_rect.center = (screen_width / 10, 712.5)

class Car():

	def __init__(self, x, y, direction, speed):
		self.direction = direction
		self.drew_new_car = False
		self.speed = speed
		self.car = random.choice(cars)
		self.rect = self.car.get_rect()
		self.rect.y = y
		self.rect.x = x
		self.length = random.randint(0,2)
		self.y_index = ys.index(self.rect.y)

	def move_car(self):
		if self.direction == 'right':
			self.rect.x += self.speed
			self.rect.right += self.speed
		if self.direction == 'left':
			self.rect.x -= self.speed
			self.rect.right -= self.speed

	def draw_car(self):
		if self.direction == 'right':
			screen.blit(pygame.transform.flip(self.car, True, False), self.rect)
		else:
			screen.blit(self.car, self.rect)

	def delete_car(self, item):
		if item in cars_created:
			cars_created.remove(item)

	def draw_new_cars(self): 
		if self.direction == 'right' and self.drew_new_car == False:
			if self.rect.right  > screen_width:
				cars_created.append(Car((-1 * self.rect.width) + 1, self.rect.y, 'right', speeds[self.y_index]))
				self.drew_new_car = True
		if self.direction == 'left' and self.drew_new_car == False:
			if self.rect.left < 0:
				cars_created.append(Car(screen_width - 1, self.rect.y, 'left', speeds[self.y_index]))
				self.drew_new_car = True


class Log():

	def __init__(self, x, y, direction, speed):
		self.log = random.choice(logs)
		self.direction = direction
		self.drew_new_log = False
		self.speed = speed
		self.rect = self.log.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.y_index = ys.index(self.rect.y)

	def move_log(self):
		if self.direction == 'right':
			self.rect.x += self.speed
			self.rect.right += self.speed
		if self.direction == 'left':
			self.rect.x -= self.speed
			self.rect.right -= self.speed

	def draw_log(self):
		screen.blit(self.log, self.rect)


	def delete_log(self, item):
		if item in logs_created:
			logs_created.remove(item)

	def draw_new_logs(self): # To address the issue of infinitely spawning in logs, put the if statements in the main game loop and only have it run this method if it meets the requirements
		if self.direction == 'right' and self.drew_new_log == False:
			if self.rect.right  > screen_width:
				logs_created.append(Log((-1 * self.rect.width) + 1, self.rect.y, 'right', speeds[self.y_index]))
				self.drew_new_log = True
		if self.direction == 'left' and self.drew_new_log == False:
			if self.rect.left < 0:
				logs_created.append(Log(screen_width - 1, self.rect.y, 'left', speeds[self.y_index]))
				self.drew_new_log = True

'''for x in x_logs:
	for y in ys:
		speed = random.choice(speeds)
		log_length = random.randint(0, 2)
		if (ys.index(y) % 2) == 0: 
			logs_created.append(Log(x, y, 'left', widths[log_length], speeds[ys.index(y)]))#widths[log_length], speed))
		else:
			logs_created.append(Log(x, y, 'right', widths[log_length], speeds[ys.index(y)])) #widths[log_length], speed))'''

def get_starting_sequence():
	global order, choice_1
	length = random.randint(0, 2)
	order = random.choice(orders)
	choice_1 = random.choice(choice)
	choice.remove(choice_1)
	choice_2 = random.choice(choice) #not so random
	choice.append(choice_1)

	for x in x_logs:
		if order == 2: #2/6
			if choice_1 == 'river':
				logs_created.append(Log(x, ys[0], 'right', speeds[0]))
				logs_created.append(Log(x, ys[1], 'left', speeds[1]))
				cars_created.append(Car(x, ys[2], 'right', speeds[2]))
				cars_created.append(Car(x, ys[3], 'left', speeds[3]))
				cars_created.append(Car(x, ys[4], 'right', speeds[4]))
				cars_created.append(Car(x, ys[5], 'left', speeds[5]))
				cars_created.append(Car(x, ys[6], 'right', speeds[6]))
				cars_created.append(Car(x, ys[7], 'left', speeds[7]))
			else:
				cars_created.append(Car(x, ys[0], 'right', speeds[0]))
				cars_created.append(Car(x, ys[1], 'left', speeds[1]))
				logs_created.append(Log(x, ys[2], 'right', speeds[2]))
				logs_created.append(Log(x, ys[3], 'left', speeds[3]))
				logs_created.append(Log(x, ys[4], 'right', speeds[4]))
				logs_created.append(Log(x, ys[5], 'left', speeds[5]))
				logs_created.append(Log(x, ys[6], 'right', speeds[6]))
				logs_created.append(Log(x, ys[7], 'left', speeds[7]))
		if order == 6: #6/2
			if choice_1 == 'street':
				cars_created.append(Car(x, ys[0], 'right', speeds[0]))
				cars_created.append(Car(x, ys[1], 'left', speeds[1]))
				cars_created.append(Car(x, ys[2], 'right', speeds[2]))
				cars_created.append(Car(x, ys[3], 'left', speeds[3]))
				cars_created.append(Car(x, ys[4], 'right', speeds[4]))
				cars_created.append(Car(x, ys[5], 'left', speeds[5]))
				logs_created.append(Log(x, ys[6], 'right', speeds[6]))
				logs_created.append(Log(x, ys[7], 'left', speeds[7]))
			else:
				logs_created.append(Log(x, ys[0], 'right', speeds[0]))
				logs_created.append(Log(x, ys[1], 'left', speeds[1]))
				logs_created.append(Log(x, ys[2], 'right', speeds[2]))
				logs_created.append(Log(x, ys[3], 'left', speeds[3]))
				logs_created.append(Log(x, ys[4], 'right', speeds[4]))
				logs_created.append(Log(x, ys[5], 'left', speeds[5]))
				cars_created.append(Car(x, ys[6], 'right', speeds[6]))
				cars_created.append(Car(x, ys[7], 'left', speeds[7]))
		if order == 5: #5/3
			if choice_1 == 'street':
				cars_created.append(Car(x, ys[0], 'right', speeds[0]))
				cars_created.append(Car(x, ys[1], 'left', speeds[1]))
				cars_created.append(Car(x, ys[2], 'right', speeds[2]))
				cars_created.append(Car(x, ys[3], 'left', speeds[3]))
				cars_created.append(Car(x, ys[4], 'right', speeds[4]))
				logs_created.append(Log(x, ys[5], 'left', speeds[5]))
				logs_created.append(Log(x, ys[6], 'right', speeds[6]))
				logs_created.append(Log(x, ys[7], 'left', speeds[7]))
			else:
				logs_created.append(Log(x, ys[0], 'right', speeds[0]))
				logs_created.append(Log(x, ys[1], 'left', speeds[1]))
				logs_created.append(Log(x, ys[2], 'right', speeds[2]))
				logs_created.append(Log(x, ys[3], 'left', speeds[3]))
				logs_created.append(Log(x, ys[4], 'right', speeds[4]))
				cars_created.append(Car(x, ys[5], 'left', speeds[5]))
				cars_created.append(Car(x, ys[6], 'right', speeds[6]))
				cars_created.append(Car(x, ys[7], 'left', speeds[7]))
		if order == 3: #3/5
			if choice_1 == 'river':
				logs_created.append(Log(x, ys[0], 'right', speeds[0]))
				logs_created.append(Log(x, ys[1], 'left', speeds[1]))
				logs_created.append(Log(x, ys[2], 'right', speeds[2]))
				cars_created.append(Car(x, ys[3], 'left', speeds[3]))
				cars_created.append(Car(x, ys[4], 'right', speeds[4]))
				cars_created.append(Car(x, ys[5], 'left', speeds[5]))
				cars_created.append(Car(x, ys[6], 'right', speeds[6]))
				cars_created.append(Car(x, ys[7], 'left', speeds[7]))
			else:
				cars_created.append(Car(x, ys[0], 'right', speeds[0]))
				cars_created.append(Car(x, ys[1], 'left', speeds[1]))
				cars_created.append(Car(x, ys[2], 'right', speeds[2]))
				logs_created.append(Log(x, ys[3], 'left', speeds[3]))
				logs_created.append(Log(x, ys[4], 'right', speeds[4]))
				logs_created.append(Log(x, ys[5], 'left', speeds[5]))
				logs_created.append(Log(x, ys[6], 'right', speeds[6]))
				logs_created.append(Log(x, ys[7], 'left', speeds[7]))
		if order == 4: #4/4
			if choice_1 == 'river':
				logs_created.append(Log(x, ys[0], 'right', speeds[0]))
				logs_created.append(Log(x, ys[1], 'left', speeds[1]))
				logs_created.append(Log(x, ys[2], 'right', speeds[2]))
				logs_created.append(Log(x, ys[3], 'left', speeds[3]))
				cars_created.append(Car(x, ys[4], 'right', speeds[4]))
				cars_created.append(Car(x, ys[5], 'left', speeds[5]))
				cars_created.append(Car(x, ys[6], 'right', speeds[6]))
				cars_created.append(Car(x, ys[7], 'left', speeds[7]))
			else:
				cars_created.append(Car(x, ys[0], 'right', speeds[0]))
				cars_created.append(Car(x, ys[1], 'left', speeds[1]))
				cars_created.append(Car(x, ys[2], 'right', speeds[2]))
				cars_created.append(Car(x, ys[3], 'left', speeds[3]))
				logs_created.append(Log(x, ys[4], 'right', speeds[4]))
				logs_created.append(Log(x, ys[5], 'left', speeds[5]))
				logs_created.append(Log(x, ys[6], 'right', speeds[6]))
				logs_created.append(Log(x, ys[7], 'left', speeds[7]))



while True:
	if gameover == False:

		FPSCLOCK = pygame.time.Clock()

		screen.fill((0, 0, 0))	
		if level == 1:
			starting_area = pygame.draw.rect(screen, (255, 128, 0), (0, 675, screen_width, screen_height / 10))
		else:
			starting_area = pygame.draw.rect(screen, (255, 255, 255), (0,675, screen_width, screen_height / 10))
		finish_area = pygame.draw.rect(screen, (255, 255, 255), (0,0, screen_width, screen_height / 10))
		score_text = FONT.render('Level ' + str(level), True, (0, 0, 0))
		screen.blit(score_text, score_text_rect)

		
		if level == 1 or level == 2:
			speeds = speeds1
		if level == 3 or level == 4:
			speeds = speeds3
		if level == 5 or level == 6:
			speeds = speeds5
		if level == 7 or level == 8:
			speeds = speeds7
		if level == 9 or level == 10:
			speeds = speeds9			


		not_in_ocean = False

		if choice_1 == 'river':
			ocean = pygame.draw.rect(screen, (0, 0, 255), (0, 75, screen_width, order * 75))
			street = pygame.draw.rect(screen, (105, 105, 105), (0, screen_height - (((8 - order) * 75) + 75), screen_width, (8 - order) * 75))

		if choice_1 == 'street':
			street = pygame.draw.rect(screen, (105, 105, 105), (0, 75, screen_width, order * 75)) 
			ocean = pygame.draw.rect(screen, (0, 0, 255), (0, screen_height - (((8 - order) * 75) + 75), screen_width, (8 - order) * 75))


		if start == True:
			get_starting_sequence()
			start = False

		for car in cars_created[:]:
			car.draw_car()
			car.move_car()
			car.draw_new_cars()
			if car.direction == 'right':
				if car.rect.left > screen_width:
					car.delete_car(car)
			if car.direction == 'left':
				if (car.rect.right) < 0:
					car.delete_car(car)

			if player_rect.colliderect(car.rect):
				gameover = True
				pygame.time.wait(100)

		for log in logs_created[:]:
			log.draw_log()
			log.move_log()
			log.draw_new_logs()


			if log.direction == 'right':
				if log.rect.left > screen_width:
					log.delete_log(log)
			if log.direction == 'left':
				if (log.rect.right) < 0:# + (log.log_width * 75)) < 0:
					log.delete_log(log)


			if player_rect.colliderect(log.rect):
				not_in_ocean = True
				if log.rect.width == 225:
				
					if abs(player_rect.centerx - log.rect.right) > abs(player_rect.centerx - log.rect.left) and abs(player_rect.centerx - log.rect.left) < abs(player_rect.centerx - log.rect.centerx):
						#Put the player on the left side
						player_rect.centerx = log.rect.left + 37.5

					if abs(player_rect.centerx - log.rect.centerx) < abs(player_rect.centerx - log.rect.right) and abs(player_rect.centerx - log.rect.centerx) < abs(player_rect.centerx - log.rect.left):
						#Put the player in the middle
						player_rect.centerx = log.rect.centerx
						
					if abs(player_rect.centerx - log.rect.right) < abs(player_rect.centerx - log.rect.left) and abs(player_rect.centerx - log.rect.centerx) > abs(player_rect.centerx - log.rect.right):
						#Put the player on the right side
						player_rect.centerx = log.rect.right - 37.5

				if log.rect.width == 150:
					if abs(player_rect.centerx - log.rect.right) > abs(player_rect.centerx - log.rect.left):
						#Put the player on the left side
						player_rect.centerx = log.rect.left + 37.5

					if abs(player_rect.centerx - log.rect.right) < abs(player_rect.centerx - log.rect.left):
						#Put the player on the right side
						player_rect.centerx = log.rect.right - 37.5

				if log.rect.width == 75:
					player_rect.centerx = log.rect.centerx

				for event in pygame.event.get():
					if event.type == KEYDOWN:
						if event.key == K_RIGHT:
							player_rect.centerx += 75
						if event.key == K_LEFT:
							player_rect.x -= 75
						if event.key == K_UP:
							#player_rect.y -= 75
							up_movement = True
						if event.key == K_DOWN:
							down_movement = True


				if log.direction == 'right':
					player_rect.x += speeds[log.y_index]
				if log.direction == 'left':
					player_rect.x -= speeds[log.y_index]
			elif starting_area.colliderect(player_rect):
				not_in_ocean = True

			elif finish_area.collidepoint((player_rect.x, player_rect.bottom)): 
				not_in_ocean = True
				level += 1
				logs_created.clear()
				cars_created.clear()
				start = True
				player_rect.top = screen_height - 68


			elif player_rect.colliderect(street):
				not_in_ocean = True

		#Gameover mechanism
		if not_in_ocean == False:
			pygame.time.wait(100)
			gameover = True

		screen.blit(player, player_rect)

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			elif event.type == KEYDOWN:
				if event.key == K_UP:
					up_movement = True
				elif event.key == K_DOWN:
					down_movement = True
				elif event.key == K_LEFT:
					left_movement = True
				elif event.key == K_RIGHT:
					right_movement = True

			#Movements
		if up_movement == True:
			if player_rect.top > 11:
				if up_movements < 75:
					player_rect.y -= 15
					up_movements += 15
				else:
					up_movements = 0
					up_movement = False
			else:
				up_movement = False
				up_movements = 0
		if down_movement == True:
			if player_rect.bottom <= screen_height - 11:
				if down_movements < 75:
					player_rect.y += 15
					down_movements += 15
				else:
					down_movements = 0
					down_movement = False
			else:
				down_movement = False
				down_movements = 0

		if left_movement == True:
			if player_rect.left > 11:
				if left_movements < 75:
					player_rect.x -= 15
					left_movements += 15
				else:
					left_movements = 0
					left_movement = False
		if right_movement == True:
			if player_rect.right <= screen_width - 11:
				if right_movements < 75:
					player_rect.x += 15
					right_movements += 15
				else:
					right_movements = 0
					right_movement = False

		if player_rect.left < 0 or player_rect.right > screen_width:
			#Gameover
			gameover = True #CAN BE USED FOR BOTH

	if gameover == True:
		screen.fill((0,0,0))
		screen.blit(gameover_text, gameover_text_rect)
		screen.blit(restart_text, restart_text_rect)
		screen.blit(FONT.render('You got to level ' + str(level), True, (255, 255, 255)), (screen_rect.centerx - 130, screen_rect.centery + 125))


		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			if event.type == KEYDOWN:
				if event.key == K_r:
					gameover = False
					player_rect.left = 300 + 11
					player_rect.top = screen_height - 68
					start = True
					logs_created.clear()
					cars_created.clear()
					up_movements = 0
					down_movements = 0
					left_movements = 0 
					right_movements = 0
					up_movement = False
					down_movement = False
					left_movement = False
					right_movement = False
					level = 1





	pygame.display.update()
	FPSCLOCK.tick(FPS)

