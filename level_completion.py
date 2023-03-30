import pygame
import mysql.connector
import label
import button
import ctypes

def level_completion(screen,level,score,loginid):
	screen.blit(box_img,(50,10))
	conn=None
	try:
		conn=mysql.connector.connect(host="remotemysql.com",port=3306,user="EGRNcrLg5M",password="I2qoHuxEz0",database="EGRNcrLg5M")
	except:
		ctypes.windll.user32.MessageBoxW(0, "Connect to internet and try again", "", 1)
		exit()
	cursor=conn.cursor()
	cursor.execute("update users set %s_score=%s where Id=%s",(level,score,loginid))
	conn.commit()
	cursor.execute(f"select (1_score+2_score+3_score+4_score+5_score+6_score+7_score+8_score+9_score) from users where Id={loginid}")
	record=cursor.fetchall()
	for rec in record:
		tot_score=rec[0]	
	label.draw(f'Total Score: {tot_score}',(0,0,0),150,150,screen,30,'Joker Man')	
	cursor.execute("update users set total_score=%s where Id=%s",(tot_score,loginid))
	conn.commit()
	if nextlevel.draw(screen):
		level_completed=level
		level+=1
		pass
	if mainmenu.draw(screen):
		pass	

	pass
