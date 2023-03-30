import pygame
import button
import pickle
import csv
pygame.init()

SCREEN_WIDTH=800
SCREEN_HEIGHT=640
LOWER_MARGIN=100
SIDE_MARGIN=300
screen=pygame.display.set_mode((SCREEN_WIDTH+SIDE_MARGIN,SCREEN_HEIGHT+LOWER_MARGIN))
pygame.display.set_caption('Level Editor')
#define game variables
scroll_left=False
scroll_right=False
scroll=0
scroll_speed=3
TILE_TYPE=24
level=0
current_tile=0
ROWS=16
MAX_COLS=200
TILE_SIZE= SCREEN_HEIGHT//ROWS
#load images
back_img=pygame.image.load('img/background/background.jfif').convert_alpha()
back_img=pygame.transform.scale(back_img,(800,640))
save_img=pygame.image.load('img/background/save.png').convert_alpha()
save_img=pygame.transform.scale(save_img,(150,60))
load_img=pygame.image.load('img/background/load.png').convert_alpha()
load_img=pygame.transform.scale(load_img,(250,130))
img_list=[]
for x in range(TILE_TYPE):
	img=pygame.image.load(f'img/background/{x}.png').convert_alpha()
	img=pygame.transform.scale(img,(TILE_SIZE,TILE_SIZE))
	img_list.append(img)
	pass

#define color
red=(255,0,0)
green=(144,201,120)
WHITE= (255,255,255)
font=pygame.font.SysFont('Futura',30)
#create empty list
world_data=[]
for row in range(ROWS):
	r=[-1]*MAX_COLS
	world_data.append(r)
	pass
for tile in range(0, MAX_COLS):
	world_data[ROWS-1][tile]=3
	world_data[ROWS-2][tile]=3
	world_data[ROWS-3][tile]=3

	pass
print(world_data)	
def draw_text(text,font,col,x,y):
	img=font.render(text,True,col)
	screen.blit(img,(x,y))
#creating background
def draw_bg():
	screen.fill(green)
	width=back_img.get_width()
	for x in range(10):
		screen.blit(back_img,((x*width)-scroll,0))
	pass
def grid():
	#vertical lines
	for c in range(MAX_COLS + 1 ):
		pygame.draw.line(screen,WHITE,(c*TILE_SIZE - scroll,0),(c*TILE_SIZE - scroll,SCREEN_HEIGHT))
		pass
	#horizontal lines	
	for c in range(ROWS + 1 ):
		pygame.draw.line(screen,WHITE,(0,c*TILE_SIZE),(SCREEN_WIDTH, c*TILE_SIZE))
		pass	
def draw_world():
	for y,row in enumerate(world_data):
		for x,tile in enumerate(row):
			if tile>=0 :
				screen.blit(img_list[tile],(x*TILE_SIZE-scroll,y*TILE_SIZE))
				pass





#create buttons
save_button=button.Button(150,650,save_img,1)
load_button=button.Button(500,650,load_img,1)
button_list=[]
button_col=0
button_row=0
for i in range(len(img_list)):
	tile_button = button.Button(SCREEN_WIDTH + (75 * button_col) + 50 , (75 * button_row + 50), img_list[i], 1)
	button_list.append(tile_button)
	button_col+=1
	if button_col==3:
		button_col=0
		button_row+=1
		pass
	pass
run=True;
button_count = 0
while run:
	draw_bg()
	grid()
	draw_world()
	draw_text(f'Level: {level}',font,WHITE,10,SCREEN_HEIGHT+LOWER_MARGIN-50)
	draw_text(f'Press up and down to change level',font,WHITE,10,SCREEN_HEIGHT+LOWER_MARGIN-30)
	abc=pygame.draw.rect(screen,green,(SCREEN_WIDTH,0,SIDE_MARGIN,SCREEN_HEIGHT))
	#choose tile
	
	for button_count, i in enumerate(button_list):
		if i.draw(screen):
			current_tile = button_count
			print(current_tile)
	pygame.draw.rect(screen, red, button_list[current_tile].rect, 3)
	if save_button.draw(screen):
		with open(f'level{level}_data.csv','w',newline='') as csvfile:
			writer=csv.writer(csvfile,delimiter=',')
			for row in world_data:
				writer.writerow(row)
	if load_button.draw(screen):
		scroll=0
		with open(f'level{level}_data.csv',newline='') as csvfile:
			reader=csv.reader(csvfile,delimiter=',')
			for x, row in enumerate(reader):
				for y, tile in enumerate(row):
					world_data[x][y]=int(tile)

	if scroll_left==True and scroll>0:
		scroll-=5 * scroll_speed
	if scroll_right==True and scroll<(MAX_COLS*TILE_SIZE)-SCREEN_WIDTH:
		scroll+=5 * scroll_speed
	#get mouse position
	pos=pygame.mouse.get_pos()
	x=(pos[0]+scroll)//TILE_SIZE
	y= pos[1] // TILE_SIZE
	if pos[0]<SCREEN_WIDTH and pos[1]<SCREEN_HEIGHT:
		if pygame.mouse.get_pressed()[0]==1:
			if world_data[y][x]!= current_tile:
				world_data[y][x]=current_tile
				pass
		if pygame.mouse.get_pressed()[2] == 1:
				world_data[y][x] = -1
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			run=False
		if event.type==pygame.KEYDOWN:
			if event.key==pygame.K_UP:
				level+=1
			if event.key==pygame.K_DOWN and level>0:
				level-=1
			if event.key==pygame.K_RIGHT:
				scroll_right=True
			if event.key==pygame.K_LEFT:
				scroll_left=True	
		if event.type==pygame.KEYUP:
			if event.key==pygame.K_LEFT:
				scroll_left=False
			if event.key==pygame.K_RIGHT:
				scroll_right=False		

	pygame.display.update()
pygame.quit()	
