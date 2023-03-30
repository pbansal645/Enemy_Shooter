import pygame
from pygame import mixer
import os
import random
import button
import login
import label
import guest
import level_selector
import csv
import mysql.connector
import time
mixer.init()
pygame.init()
SCREEN_WIDTH=800
SCREEN_HEIGHT=int(SCREEN_WIDTH*0.8)
screen= pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Shooter')
guest_no=0
#det frame rate
clock=pygame.time.Clock()
FPS=80
gravity = 0.5
scroll_thresh=200
ROWS=16
COLS=200
TILE_SIZE= SCREEN_HEIGHT//ROWS
TILE_TYPE=24
shoot=False
grenade=False
grenade_thrown=False
level=1
level_completed=0
TOTAL_SCORE=0
start_game=False
login_check=False
screen_scroll=0
bg_scroll=0
#define action variables
moving_left=False
moving_right=False
bg_img=pygame.image.load('img/extra/background5.png')
bg_img=pygame.transform.scale(bg_img,(SCREEN_WIDTH,SCREEN_HEIGHT))
back_img=pygame.image.load('img/background/background.jfif').convert_alpha()
back_img=pygame.transform.scale(back_img,(800,640))
# buttons images
restart_img=pygame.image.load('img/button/restart.png').convert_alpha()
box_img=pygame.image.load('img/extra/board3.png')
box_img=pygame.transform.scale(box_img,(700,600))
box1_img=pygame.image.load('img/extra/board4.png')
box1_img=pygame.transform.scale(box1_img,(600,500))
nextlevel_img=pygame.image.load('img/button/nextlevel.png')
mainmenu_img=pygame.image.load('img/button/mainmenu.png').convert_alpha()
login_img=pygame.image.load('img/button/login.png').convert_alpha()
guest_img=pygame.image.load('img/button/guest.png').convert_alpha()
#item box image
bulletbox_img=pygame.image.load('img/icons/bullet.png').convert_alpha()
bulletbox_img=pygame.transform.scale(bulletbox_img,(25,25))
grenadebox_img=pygame.image.load('img/icons/grenade.png').convert_alpha()
grenadebox_img=pygame.transform.scale(grenadebox_img,(25,25))
healthbox_img=pygame.image.load('img/icons/health.png').convert_alpha()
healthbox_img=pygame.transform.scale(healthbox_img,(25,25))
coin_img=pygame.image.load('img/background/17.png').convert_alpha()
coin_img=pygame.transform.scale(coin_img,(30,30))
item_boxes={
	'Health'	: healthbox_img,
	'Bullet'	: bulletbox_img,
	'Grenade'	: grenadebox_img,
	'Coin'		: coin_img
}
#buulet image
bullet_image=pygame.image.load('img/bullet.png').convert_alpha()
bullet_image=pygame.transform.scale(bullet_image,(8,8))
bullet1_image=pygame.image.load('img/icons/bullet1.png').convert_alpha()
bullet1_image=pygame.transform.scale(bullet1_image,(10,22))
#grenade image
grenade_image=pygame.image.load('img/grenade.png').convert_alpha()
grenade_image=pygame.transform.scale(grenade_image,(10,10))
# world data images
img_list=[]
for x in range(TILE_TYPE):
	img=pygame.image.load(f'img/background/{x}.png').convert_alpha()
	img=pygame.transform.scale(img,(TILE_SIZE,TILE_SIZE))
	img_list.append(img)
	pass
#define colors
BG= (144,201,120)
ORANGE=(255,140,0)
RED=(255,0,0)
GREEN=(0, 255, 0)
WHITE=(255,255,255)
font=pygame.font.SysFont('Futura',25)
def draw_bars():
	ammo_bar_img=bulletbox_img
	ammo_bar_img= pygame.transform.scale(ammo_bar_img,(25,25))
	screen.blit(ammo_bar_img,(5,5))
	grenade_bar_img=grenadebox_img
	grenade_bar_img= pygame.transform.scale(grenade_bar_img,(25,25))
	screen.blit(grenade_bar_img,(5,35))	
	screen.blit(bullet1_image,(40,5))
	grenade_img=grenade_image
	grenade_img= pygame.transform.scale(grenade_img,(15,20))
	screen.blit(grenade_img,(40,35))
	img=font.render(f'X {player.ammo}',True, WHITE)
	screen.blit(img,(60,5))
	img1=font.render(f'X {player.grenades}',True, WHITE)
	screen.blit(img1,(60,35))
	img2=font.render(f'Score:  {player.score}',True, WHITE)
	screen.blit(img2,(700,5))
	img3=font.render(f'Time:  {player.elapsed_time}',True, WHITE)
	screen.blit(img3,(600,5))
#function to fill background color
def draw_bg():
	width=back_img.get_width()
	for x in range(10):
		screen.blit(back_img,((x*width)-bg_scroll*0.5,0))
	pass
#function to create a player or enemy
def reset_level():
	enemy_group.empty()
	bullet_group.empty()
	grenade_group.empty()
	explosion_group.empty()
	item_box_group.empty()
	decorations_group.empty()
	water_group.empty()
	exit_box_group.empty()
	data=[]
	for row in range(ROWS):
		r=[-1]*COLS
		data.append(r)
		pass
	return data	
	pass
class Soldier(pygame.sprite.Sprite) :
	def __init__(self, char, x, y, scale, speed,ammo,grenades):
		pygame.sprite.Sprite.__init__(self)
		#character type
		self.char=char
		self.alive=True
		self.speed=speed
		self.ammo=ammo
		self.start_ammo=ammo
		self.shoot_cooldown=0
		self.grenades=grenades
		self.health=100
		self.max_health=self.health
		self.direction=1
		self.in_air=True
		self.flip=False
		self.jump=False
		self.vel_y=0
		self.death_counter=0
		self.animatio_list=[]
		self.frame_index=0
		self.action =0 
		self.update_time=pygame.time.get_ticks()
		self.score=0
		# creating ai variabkes
		self.move_counter=0
		self.vision=pygame.Rect(0,0,150,20)
		self.idle=False
		self.idle_counter=0
		self.time=time.time()
		self.elapsed_time=0
		animation_type=['idle','run','jump','diet']
		for animation in animation_type:
			nu_of_frame=len(os.listdir(f'img/{self.char}/{animation}'))
			temp_list = []
			for i in range(nu_of_frame):
				img = pygame.image.load(f'img/{self.char}/{animation}/{i}.png').convert_alpha()
				img = pygame.transform.scale(img, (int(img.get_width()*scale),TILE_SIZE))
				temp_list.append(img)
			self.animatio_list.append(temp_list)
			pass
		self.image=self.animatio_list[self.action][self.frame_index]
		self.rect= self.image.get_rect()
		self.rect.center = (x,y)
		self.width=self.image.get_width()
		self.height=self.image.get_height()
	def update(self):
		self.update_animation()
		self.check_alive()
		if self.shoot_cooldown>0:
			self.shoot_cooldown-=1
	def move(self, move_left, move_right):
		screen_scroll=0
		dx=0
		dy=0
		if move_left:
			dx= -self.speed
			self.flip=True
			self.direction=-1
		if move_right:
			dx=self.speed
			self.flip=False
			self.direction=1
		if self.jump == True and self.in_air==False: 
			self.vel_y=-11
			self.jump=False
			self.in_air=True
		self.vel_y += gravity
		if self.vel_y > 10: 		
			self.vel_y
		dy += self.vel_y	
		#check collision
		for tile in world.obstacle_list:
			if tile[1].colliderect(self.rect.x+dx,self.rect.y,self.width,self.height):
				dx=0
				if self.char=='enemy':
					self.direction*=-1
					self.move_counter=0
					pass
			if tile[1].colliderect(self.rect.x,self.rect.y+dy,self.rect.width,self.height):
				if self.vel_y<0:
					self.vel_y=0
					dy=tile[1].bottom-self.rect.top
				elif self.vel_y>=0:
					self.vel_y=0
					self.in_air=False
					dy=tile[1].top-self.rect.bottom
		if pygame.sprite.spritecollide(self,water_group,False):
			player.health=0
		level_complete=False	
		if pygame.sprite.spritecollide(self,exit_box_group,False):
			dx=0
			level_complete=True
		if level_complete==False:
			self.elapsed_time=int(time.time()-self.time)
		if self.rect.bottom>SCREEN_HEIGHT:
			player.health=0					
		if self.char=='player':
			if (self.rect.left + dx<0 or self.rect.right+dx>SCREEN_WIDTH):
				dx=0						
		self.rect.x += dx
		self.rect.y += dy
		if self.char=='player':
			if(self.rect.right>SCREEN_WIDTH-scroll_thresh and bg_scroll<(world.level_length*TILE_SIZE)-SCREEN_WIDTH) or (self.rect.left<scroll_thresh and bg_scroll>abs(dx)):
				self.rect.x-=dx
				screen_scroll=-dx
		return screen_scroll,level_complete
	def shoot(self):
		if self.shoot_cooldown==0 and self.ammo>0:
			self.shoot_cooldown=20
			bullet=Bullet(self.rect.centerx+(0.75*self.rect.size[0]*self.direction),self.rect.centery-9,self.direction)
			bullet_group.add(bullet)
			self.ammo-=1
	def ai(self):		
		if self.alive and player.alive:
			if self.idle==False and random.randint(1, 500)==1:
				self.update_action(0)
				self.idle=True
				self.idle_counter=30
			if self.vision.colliderect(player.rect):
				self.update_action(0)
				self.shoot()
			else:		
				if self.idle==False:
					if self.direction==1:
						ai_moving_right=True
					else:	
						ai_moving_right=False
					ai_moving_left=not ai_moving_right
					self.move(ai_moving_left,ai_moving_right)
					self.update_action(1)	
					self.move_counter+=1
					self.vision.center=(self.rect.centerx+75 * self.direction,self.rect.centery)
					if self.move_counter>10:
						self.direction*= -1
						self.move_counter*=-1
						pass
				else:		
					self.idle_counter-=1
					if self.idle_counter<=0:
						self.idle=False
						pass
		self.rect.x+=screen_scroll		
	def update_animation(self):
		Animation_cool=150
		self.image=self.animatio_list[self.action][self.frame_index]
		if pygame.time.get_ticks() - self.update_time > Animation_cool:
			self.frame_index +=1
			self.update_time=pygame.time.get_ticks()
		if self.frame_index >= len(self.animatio_list[self.action]):
			if self.action==3:
				self.frame_index=len(self.animatio_list[self.action])-1
			else:	
				self.frame_index=0
	def update_action(self, new_action):
		if(new_action != self.action):
			self.action=new_action
			self.frame_index=0
			self.update_time=pygame.time.get_ticks()
	def check_alive(self):
		if self.health<=0:
			self.health=0
			self.speed=0
			self.alive=False
			self.update_action(3)
	def health_bar(self):
		pygame.draw.rect(screen,(204, 255, 255),pygame.Rect(self.rect.left,self.rect.top-20,80,10),0,10)
		health_bar=(self.health/self.max_health)*80;
		if(self.health>75):
			color=GREEN
		elif (self.health>50):	
			color=ORANGE
		else :	
			color=RED
		pygame.draw.rect(screen,color,pygame.Rect(self.rect.left,self.rect.top-20,health_bar,10),0,10)
				
	def draw(self):
		screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
		self.health_bar()	
class World():
	def __init__(self):
		self.obstacle_list=[]
	def process_data(self, data):
		self.level_length=len(data[1])
		for y,row in enumerate(data):
			for x,tile in enumerate(row):
				if tile>=0:
					img=img_list[tile]
					img_rect=img.get_rect()
					img_rect.x=x*TILE_SIZE
					img_rect.y=y*TILE_SIZE
					tile_data=(img,img_rect)
					if tile>=0 and tile<=8:
						self.obstacle_list.append(tile_data)
					elif (tile>=9 and tile<=10 or tile==16):
						water=Water(img,x*TILE_SIZE,y*TILE_SIZE)
						water_group.add(water)
					elif tile>=11 and tile<=13:
						decorations=Decorations(img,x*TILE_SIZE,y*TILE_SIZE)
						decorations_group.add(decorations)
					elif (tile==21):
						player=Soldier('player',x*TILE_SIZE,y*TILE_SIZE,0.35,3, 20,5)
					elif (tile==22):
						enemy=Soldier('enemy',x*TILE_SIZE,y*TILE_SIZE,1,2, 100,0)
						enemy_group.add(enemy)
					elif tile==17:	
						item_box=Itembox('Coin',x*TILE_SIZE,y*TILE_SIZE)
						item_box_group.add(item_box)
					elif (tile==18):
						item_box=Itembox('Bullet',x*TILE_SIZE,y*TILE_SIZE)
						item_box_group.add(item_box)
					elif (tile==20):
						item_box=Itembox('Health',x*TILE_SIZE,y*TILE_SIZE)
						item_box_group.add(item_box)
					elif (tile==19):
						item_box=Itembox('Grenade',x*TILE_SIZE,y*TILE_SIZE)
						item_box_group.add(item_box)
					elif (tile==23):
						exit_box=exit(img,x*TILE_SIZE,y*TILE_SIZE)
						exit_box_group.add(exit_box)	
		return player				
	def draw(self):		
		for tile in self.obstacle_list:
			tile[1][0]+=screen_scroll
			screen.blit(tile[0],tile[1])
class Decorations(pygame.sprite.Sprite):
	def __init__(self,img,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image=img
		self.rect=self.image.get_rect()
		self.rect.midtop=(x+TILE_SIZE//2,y+(TILE_SIZE-self.image.get_height()))
	def update(self):	
		self.rect.x+=screen_scroll
class exit(pygame.sprite.Sprite):
	def __init__(self,img,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image=img
		self.rect=self.image.get_rect()
		self.rect.midtop=(x+TILE_SIZE//2,y+(TILE_SIZE-self.image.get_height()))
	def update(self):	
		self.rect.x+=screen_scroll		
class Water(pygame.sprite.Sprite):
	def __init__(self,img,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image=img
		self.rect=self.image.get_rect()
		self.rect.center=(x+TILE_SIZE//2,y+TILE_SIZE//2)
	def update(self):	
		self.rect.x+=screen_scroll		
class Itembox(pygame.sprite.Sprite):
	"""docstring for Itembox"""
	def __init__(self,item_type, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.item_type=item_type
		self.image=item_boxes[self.item_type]
		self.rect=self.image.get_rect()
		self.rect.midtop=(x+(TILE_SIZE//2),y+(TILE_SIZE-self.image.get_height()))
	def update(self):	
		self.rect.x+=screen_scroll
		if pygame.sprite.collide_rect(self,player):
			if self.item_type=='Health':
				player.health+=25
				if player.health>player.max_health:
					player.health=player.max_health
					pass
			elif self.item_type=='Bullet':	
				player.ammo+=15
			elif self.item_type=='Grenade':	
				player.grenades+=3
			elif self.item_type=='Coin':
				player.score+=5
			self.kill()
class Bullet(pygame.sprite.Sprite):
	"""docstring for Bullet"""
	def __init__(self, x, y, direction):
		pygame.sprite.Sprite.__init__(self)
		self.speed = 10
		self.image=bullet_image
		self.rect=self.image.get_rect()
		self.rect.center=(x,y)
		self.direction=direction
	def update(self):
		self.rect.x+=(self.direction*self.speed)+screen_scroll
		if self.rect.right<0 or self.rect.left>SCREEN_WIDTH:
			self.kill()
		for tile in world.obstacle_list:
			if tile[1].colliderect(self.rect):
				self.kill()
				pass	
		if pygame.sprite.spritecollide(player, bullet_group,False):
			if player.alive:
				player.health-=5
				self.kill()
		for enemy in enemy_group:
			if pygame.sprite.spritecollide(enemy, bullet_group, False):
				if enemy.alive:
					enemy.health-=25
					self.kill()	
class Grenade(pygame.sprite.Sprite):
	"""docstring for Grenade"""
	def __init__(self, x, y, direction):
		pygame.sprite.Sprite.__init__(self)
		self.timer=100
		self.vel_y=-11
		self.speed = 5
		self.image=grenade_image
		self.rect=self.image.get_rect()
		self.rect.center=(x,y)
		self.direction=direction
		self.width=self.image.get_width()
		self.height=self.image.get_height()
	def update(self):
		self.vel_y+=gravity
		dx=self.speed*self.direction
		dy=self.vel_y
		for tile in world.obstacle_list:
			if tile[1].colliderect(self.rect.x+dx,self.rect.y,self.width,self.height):
				self.direction*=-1
				dx=self.direction*self.speed
			if tile[1].colliderect(self.rect.x,self.rect.y+dy,self.width,self.height):
				if self.vel_y<0:
					self.vel_y=0
					dy=tile[1].bottom-self.rect.top
				elif self.vel_y>=0:
					self.vel_y=0
					dy=tile[1].top-self.rect.bottom
				self.speed=0	
				
				
		self.rect.x+=dx+screen_scroll
		self.rect.y+=dy
		self.timer-=1
		if self.timer<=0:
			self.kill()
			explosion=Explosion(self.rect.x,self.rect.y-20,1)
			explosion_group.add(explosion)
			if abs(self.rect.x-player.rect.centerx)<TILE_SIZE*2 and \
			abs(self.rect.y-player.rect.centery)<TILE_SIZE* 2 :
				player.health-=50
			for enemy in enemy_group:
				if abs(self.rect.x-enemy.rect.centerx)<TILE_SIZE*2 and \
				abs(self.rect.y-enemy.rect.centery)<TILE_SIZE* 2 :
					enemy.health-=50	
class Explosion(pygame.sprite.Sprite):
	"""docstring for Bullet"""
	def __init__(self, x, y,scale):
		pygame.sprite.Sprite.__init__(self)
		self.images=[]
		for num in range(0,23):
			img=pygame.image.load(f'img/explosion/exp{num}.png').convert_alpha()
			img=pygame.transform.scale(img,(int(img.get_width()*scale),int(img.get_height()*scale)))
			self.images.append(img)
			pass
		self.frame_index=0	
		self.image=self.images[self.frame_index]
		self.rect=self.image.get_rect()
		self.rect.center=(x,y)
		self.counter=0
	def update(self):
		self.rect.x+=screen_scroll
		EXPLOSION_SPEED=4
		self.counter+=1
		if self.counter>=EXPLOSION_SPEED:
			self.counter=0
			self.frame_index+=1
			if self.frame_index>=len(self.images):
				self.kill()
			else:
				self.image=self.images[self.frame_index]
#create sprite groups
enemy_group=pygame.sprite.Group()
bullet_group=pygame.sprite.Group()
grenade_group=pygame.sprite.Group()
explosion_group=pygame.sprite.Group()
item_box_group=pygame.sprite.Group()
decorations_group=pygame.sprite.Group()
water_group=pygame.sprite.Group()
exit_box_group=pygame.sprite.Group()
#create buttons
nextlevel=button.Button(100,520,nextlevel_img,1)
restart_button=button.Button(250,320,restart_img,1)
mainmenu_button=button.Button(250,450,mainmenu_img,1)
login_button=button.Button(250,300,login_img,1)
guest_button=button.Button(250,450,guest_img,1)
mainmenu=button.Button(400,520,mainmenu_img,1)
#create empty list
world_data=[]
for row in range(ROWS):
	r=[-1]*COLS
	world_data.append(r)
	pass
record=[]	
timer=time.time()
run=True
while run:
	clock.tick(FPS)
	if login_check==False:
		screen.blit(bg_img,(0,0))
		world_data=reset_level()
		if login_button.draw(screen):		
			login_check,run,record=login.loop(screen)
		elif guest_button.draw(screen):
			uid,name,record=guest.create_guest()
			pygame.time.delay(200)
			login_check=True
	elif login_check==True:
		for rec in record:
			uid=rec[0]
			uname=rec[1]
			level_completed=rec[26]
		if start_game==False:
			run,start_game,level,login_check=level_selector.draw(screen,level_completed,record)
			with open(f'level{level}_data.csv',newline='') as csvfile:
				reader=csv.reader(csvfile,delimiter=',')
				for x, row in enumerate(reader):
					for y, tile in enumerate(row):
						world_data[x][y]=int(tile)
			world=World()
			player=world.process_data(world_data)
		else:	
			draw_bg()
			world.draw()
			player.draw()	
			draw_bars()
			player.update()
			for enemy in enemy_group:
				enemy.ai()
				enemy.update()
				enemy.draw()
			#update and draw groups
			bullet_group.update()
			grenade_group.update()
			explosion_group.update()
			item_box_group.update()
			exit_box_group.update()
			decorations_group.update()
			water_group.update()
			bullet_group.draw(screen)
			grenade_group.draw(screen)
			explosion_group.draw(screen)
			item_box_group.draw(screen)
			exit_box_group.draw(screen)
			decorations_group.draw(screen)
			water_group.draw(screen)	
			#updating player action
			if player.alive:
				#shoot bullets
				if shoot:
					player.shoot()
				elif grenade and grenade_thrown==False and player.grenades>0:
					grenade=Grenade(player.rect.centerx+(0.5*player.rect.size[0]*player.direction),player.rect.centery-9,player.direction)
					grenade_group.add(grenade)
					grenade_thrown=True
					player.grenades-=1
				if player.in_air:
					player.update_action(2)
				elif moving_left or moving_right:
					player.update_action(1)
				else:
					player.update_action(0)	
				screen_scroll,level_complete=player.move(moving_left, moving_right)
				bg_scroll-=screen_scroll
				if level_complete:
					if level>=level_completed:
							level_completed+=1			
					screen.blit(box_img,(50,10))
					conn=mysql.connector.connect(host="remotemysql.com",port=3306,user="EGRNcrLg5M",password="I2qoHuxEz0",database="EGRNcrLg5M")
					cursor=conn.cursor()
					cursor.execute("update users set %s_score=%s,%s_time=%s,Levelcompleted=%s where Id=%s",(level+1,player.score,level+1,player.elapsed_time,level_completed,uid))
					conn.commit()
					cursor.execute(f"select (1_score+2_score+3_score+4_score+5_score+6_score+7_score+8_score+9_score),(1_time+2_time+3_time+4_time+5_time+6_time+7_time+8_time+9_time) from users where Id={uid}")
					record=cursor.fetchall()
					for rec in record:
						tot_score=rec[0]	
						tot_time=rec[1]
					label.draw(f'{tot_score}',(0,0,0),270,140,screen,28,'Joker Man')
					cursor.execute("update users set Totalscore=%s,Totaltime=%s where Id=%s",(tot_score,tot_time,uid))
					conn.commit()
					cursor.execute("select Id,Totalscore from users order by Totalscore desc")
					record=cursor.fetchall()
					count=0
					for rec in record:
						count+=1
						if rec[0]==uid:
							rank=count
							pass
					label.draw(f'{rank}',(0,0,0),570,140,screen,28,'Joker Man')	
					cursor.execute("select Name,Totalscore from users order by Totalscore desc limit 3")
					record=cursor.fetchall()
					i=0
					for rec in record:
						label.draw(f'{rec[0]}',(0,0,0),250,270+i,screen,28,'Joker Man')
						label.draw(f'{rec[1]}',(0,0,0),550,270+i,screen,28,'Joker Man')
						i+=70
						pass	
					cursor.execute(f"select * from users where Id={uid}")
					record=cursor.fetchall()	
					if nextlevel.draw(screen):
						level+=1
						bg_scroll=0
						world_data=reset_level()
						with open(f'level{level}_data.csv',newline='') as csvfile:
							reader=csv.reader(csvfile,delimiter=',')
							for x, row in enumerate(reader):
								for y, tile in enumerate(row):
									world_data[x][y]=int(tile)
						world=World()
						player=world.process_data(world_data)
					if mainmenu.draw(screen):
						run,start_game,level,login_check=level_selector.draw(screen,level_completed,record)
						bg_scroll=0
						world_data=reset_level()
						with open(f'level{level}_data.csv',newline='') as csvfile:
							reader=csv.reader(csvfile,delimiter=',')
							for x, row in enumerate(reader):
								for y, tile in enumerate(row):
									world_data[x][y]=int(tile)
						world=World()
						player=world.process_data(world_data)
						pass	
			else:
				screen_scroll=0
				screen.blit(box1_img,(100,100))

				if restart_button.draw(screen):
					bg_scroll=0
					world_data=reset_level()
					with open(f'level{level}_data.csv',newline='') as csvfile:
						reader=csv.reader(csvfile,delimiter=',')
						for x, row in enumerate(reader):
							for y, tile in enumerate(row):
								world_data[x][y]=int(tile)
					world=World()
					player=world.process_data(world_data)
				if mainmenu_button.draw(screen):
						run,start_game,level,login_check=level_selector.draw(screen,level_completed,record)
						bg_scroll=0
						world_data=reset_level()
						with open(f'level{level}_data.csv',newline='') as csvfile:
							reader=csv.reader(csvfile,delimiter=',')
							for x, row in enumerate(reader):
								for y, tile in enumerate(row):
									world_data[x][y]=int(tile)
						world=World()
						player=world.process_data(world_data)
						pass	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
		    run=False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a:
				moving_left=True
			if event.key == pygame.K_SPACE:
				shoot=True	
			if event.key == pygame.K_q:
				grenade=True			
			if event.key == pygame.K_d:
				moving_right=True
			if event.key == pygame.K_w and player.alive:
				player.jump=True
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_a:
				moving_left=False
			if event.key == pygame.K_d:
				moving_right=False	
			if event.key == pygame.K_q:
				grenade=False	
				grenade_thrown=False
			if event.key == pygame.K_SPACE:
				shoot=False
	pygame.display.update()			
pygame.quit()		