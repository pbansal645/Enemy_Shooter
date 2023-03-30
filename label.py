import pygame
pygame.init()

def draw(text,col,x,y,screen,size,font):
	font=pygame.font.SysFont(font,size,True)
	img=font.render(text,True,col)
	screen.blit(img,(x,y))