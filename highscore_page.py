import pygame
import button
import mysql.connector
import label
import ctypes
bg_img=pygame.image.load('img/extra/background2.jpg')
bg_img=pygame.transform.scale(bg_img,(800,int(800*0.8)))
box_img=pygame.image.load('img/extra/scoreboard.png')
box_img=pygame.transform.scale(box_img,(600,500))
back_img=pygame.image.load('img/button/back.png')
back_img=pygame.transform.scale(back_img,(50,50))
back=button.Button(170,130,back_img,1)
def loop(screen):
	loop=True
	while loop:
		screen.blit(bg_img,(0,0))
		screen.blit(box_img,(100,100))
		conn=None
		try:
			conn=mysql.connector.connect(host="remotemysql.com",port=3306,user="EGRNcrLg5M",password="I2qoHuxEz0",database="EGRNcrLg5M")
		except:
			ctypes.windll.user32.MessageBoxW(0, "Connect to internet and try again", "", 1)
			exit()
		cursor=conn.cursor()
		cursor.execute("select Name,Totalscore from users order by Totalscore desc limit 6")
		record=cursor.fetchall()
		i=0
		for rec in record:
			label.draw(f'{rec[0]}',(0,0,0),260,210+i,screen,28,'Joker Man')
			label.draw(f'{rec[1]}',(0,0,0),520,210+i,screen,28,'Joker Man')
			i+=60
			pass
		if back.draw(screen):
			loop=False
			pygame.time.delay(200)
			pass
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				loop=False
		pygame.display.update()


		pass