import pygame
import label
import button
import help_page
import highscore_page
pygame.init()
SCREEN_WIDTH=800
SCREEN_HEIGHT=int(SCREEN_WIDTH*0.8)
img_list=[]
active_img_list=[]
inactive_img_list=[]
#bg_img=pygame.image.load('img/extra/box.png')
#bg_img1=pygame.image.load('img/extra/box1.png')
bg_img=pygame.image.load('img/extra/background4.jpg')
bg_img=pygame.transform.scale(bg_img,(SCREEN_WIDTH,SCREEN_HEIGHT))
play_img=pygame.image.load('img/button/play.png')
help_img=pygame.image.load('img/button/help.png')
logout_img=pygame.image.load('img/button/logout.png')
highscore_img=pygame.image.load('img/button/highscore.png')
for x in range(9):
	img=pygame.image.load('img/button/inactive_level.png')
	img=pygame.transform.scale(img,(80,80))
	inactive_img_list.append(img)
	pass
for x in range(9):
	img=pygame.image.load(f'img/button/{x}.png')
	img=pygame.transform.scale(img,(80,80))
	active_img_list.append(img)
	pass	
abutton_list=[]
def draw(screen,level_completed,record):
	
	level_completed=level_completed
	button_list=[]
	button_col=0
	button_row=0
	abutton_col=0
	abutton_row=0
	current_level=0
	run=True
	for i in range(level_completed+1):
		tile_button = button.Button((100 * button_col) + 450 , (150 * button_row) + 220, active_img_list[i], 1)
		button_list.append(tile_button)
		button_col+=1
		if button_col==3:
			button_col=0
			button_row+=1
	play_button=button.Button(50 , 500, play_img, 1)	
	help_button=button.Button(50 , 370, help_img, 1)	
	highscore_button=button.Button(50 , 220, highscore_img, 1)
	logout_button=button.Button(50 , 70, logout_img, 1)		
	while run:	
		screen.blit(bg_img,(0,0))
		img_col=3
		img_row=3
		button_col=0
		button_row=0
		for x in range(len(inactive_img_list)-level_completed-1):
			screen.blit(inactive_img_list[x],((100 * img_col) +350 , (130 * img_row )+100))
			img_col-=1
			if img_col==0:
				img_col=3
				img_row-=1
			pass
		for rec in record:
			for x in range(8,level_completed+9):
				label.draw(f'{rec[x]}',(255,255,255),(100 * button_col) + 470 , (140 * button_row) + 310,screen,34,'Copper')
				label.draw(f'{rec[x+9]} s',(255,255,255),(100 * button_col) + 460 , (150 * button_row) + 200,screen,24,'Copper')	
				button_col+=1
				if button_col==3:
					button_col=0
					button_row+=1
			label.draw(f'{rec[1]}',(255,255,255),70,25,screen,36,'Joker Man')
			label.draw(f'{rec[6]}',(255,255,255),730,130,screen,24,'Copper')
			label.draw(f'{rec[7]} s',(255,255,255),730,170,screen,24,'Copper')	
		for button_count, i in enumerate(button_list):
			if i.draw(screen):
				current_level=button_count
		pygame.draw.rect(screen, (255,255,255), button_list[current_level].rect, 3)		
		if play_button.draw(screen):
			return True,True,current_level,True
			pass
		if help_button.draw(screen):
			help_page.loop(screen)
			pass	
		if highscore_button.draw(screen):
			highscore_page.loop(screen)	
		if logout_button.draw(screen):
			return True,False,current_level,False			
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				return False,False,current_level,False
		pygame.display.update()
	
