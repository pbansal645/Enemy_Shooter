import pygame
import button
import textbox
import label
import register
import mysql.connector
import ctypes
bg_img=pygame.image.load('img/extra/background2.jpg')
bg_img=pygame.transform.scale(bg_img,(800,int(800*0.8)))
login_img=pygame.image.load('img/button/login.png')
login_img=pygame.transform.scale(login_img,(150,80))
back_img=pygame.image.load('img/button/back.png')
back_img=pygame.transform.scale(back_img,(50,50))
register_img=pygame.image.load('img/button/register.png')
register_img=pygame.transform.scale(register_img,(150,65))
box_img=pygame.image.load('img/extra/box.png')

button1=button.Button(200,420,login_img,1)
button2=button.Button(350,425,register_img,1)
back=button.Button(170,170,back_img,1)

BG= (144,201,120)
def draw_bg(screen):
	screen.blit(bg_img,(0,0))
	screen.blit(box_img,(100,100))

	pass
def checkdata(username,password,screen):
	record=[]
	uid=0
	uname=0
	levelcompleted=0
	if username=='':
		msg1="Email is empty"
		return False,record,msg1
		pass
	elif password=='':
		msg1="Password is empty"
		return False,record,msg1
		pass	
	else:	
		conn=None
		try:
			conn=mysql.connector.connect(host="remotemysql.com",port=3306,user="EGRNcrLg5M",password="I2qoHuxEz0",database="EGRNcrLg5M")
		except:
			ctypes.windll.user32.MessageBoxW(0, "Connect to internet and try again", "", 1)
			exit()
		cursor=conn.cursor()
		cursor.execute("select * from users where Email=%s AND Password=%s",(username,password))
		record=cursor.fetchall()
		if record:
			msg2="Login Sucessfull"
			return True,record,msg2
		else:
			msg3="Email & password does not match"
			return False,record,msg3
		cursor.close()
		conn.close()	
			
def loop(screen):
	login=True
	username=textbox.Textbox(screen,220,270,280,40)
	password=textbox.Textbox(screen,220,360,280,40)
	check=True
	record=[]
	while login:
		draw_bg(screen)
		username.draw('simple')
		password.draw('password')
		label.draw('Login',(255,255,255),250,150,screen,60,'Arial Black')
		label.draw('Email :',(255,255,255),170,230,screen,36,'Cambria')
		label.draw('Password: ',(255,255,255),170,320,screen,36,'Cambria')
		if check==False:
			label.draw(msg,(255,255,255),190,550,screen,28,'Cambria')
			pass
		pos=pygame.mouse.get_pos()
		username.update(pos)
		password.update(pos)
		if button1.draw(screen):
			uname=username.gettext()
			passw=password.gettext()
			checklogin,record,msg=checkdata(uname,passw,screen)
			if checklogin:
				pygame.time.delay(500)
				check=True
				return True,True,record
			else:	
				check=False
		if button2.draw(screen):
			register.loop(screen)
		if back.draw(screen):
			return False,True,record
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				return False,False,record
			if event.type==pygame.KEYDOWN:
				username.user_input(event)
				password.user_input(event)

		pygame.display.update()
				

	pass