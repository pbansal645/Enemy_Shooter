import pygame
import mysql.connector

import ctypes
def create_guest():
	conn=None
	try:
		conn=mysql.connector.connect(host="remotemysql.com",port=3306,user="EGRNcrLg5M",password="I2qoHuxEz0",database="EGRNcrLg5M")
	except:
		ctypes.windll.user32.MessageBoxW(0, "Connect to internet and try again", "", 1)
		exit()
	cursor=conn.cursor()

	cursor.execute("insert into users (Name,Email) values('','')")
	conn.commit()
	cursor.execute("select * from users where Email=''")
	record=cursor.fetchall()
	for rec in record:
		gid=rec[0]
	guest_name="Guest"+f'{gid}'	
	cursor.execute("update users set Name=%s,Email=%s where id=%s",(guest_name,guest_name,gid))
	conn.commit()
	cursor.close()
	conn.close()
	gid,name,record=get_data(guest_name)
	return gid,name,record


def get_data(guest_name):
	guest=guest_name
	conn1=None
	try:
		conn1=mysql.connector.connect(host="remotemysql.com",port=3306,user="EGRNcrLg5M",password="I2qoHuxEz0",database="EGRNcrLg5M")
	except:
		ctypes.windll.user32.MessageBoxW(0, "Connect to internet and try again", "", 1)
		exit()
	cursor1=conn1.cursor()
	cursor1.execute(f"select * from users where Email='{guest}'")
	record=cursor1.fetchall()
	for rec in record:
		gid=rec[0]
		name=rec[1]
	return gid,name,record	
	cursor1.close()
	conn1.close()
	