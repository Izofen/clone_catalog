#!/usr/bin/python
# -*- coding: utf-8
# Информация сохраняется в базу данных.

print ('[+] Программа регистрации новых клиентов')
print ('[+] Версия 3.1')
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
#import iz_func
import time
api_id       = 192804
api_hash     = '1b40d1d01f8922b384d44e29d32f6acf'
lbl = 'Новый клиент'
phone_number = input('    [?] Enter a phone_number (+79033671563) -> ')
#db,cursor = iz_func.connect ()
#sql = "select id,name,session from telegram_session where name = '"+str(phone_number)+"' limit 1"
#cursor.execute(sql)
#data = cursor.fetchall()
#for rec in data: 
#	lbl = "Клиент обнаружен"    
#if lbl == 'Новый клиент':
#    print ('    [+]',lbl)

def connect (connect_info):
    import pymysql 
    db = pymysql.connect(host=connect_info['host'],user=connect_info['user'],password=connect_info['password'],database=connect_info['database'],charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)  
    cursor = db.cursor() 
    return db,cursor


if 1==1:
    with TelegramClient(StringSession(), api_id, api_hash) as client:
        session = client.session.save()
        unixtime = int(time.time())
        #db,cursor = iz_func.connect ()
        print ('[+] session',session)

        host = '127.0.0.1'       
        user = 'izofen'
        password = 'podkjf4'
        database = 'telegram'
        connect_info = {'host':host,'user':user,'password':password,'database':database} 
        db,cursor = connect (connect_info)

        sql = "INSERT INTO accound (`name`,`data_id`,`info`,`status`) VALUES ('new',100,'{}','')".format (session)
        print ('[sql]:',sql)
        cursor.execute(sql)
        db.commit()  
        lastid = cursor.lastrowid
        print ('[lastid]',lastid)

        sql = "UPDATE accound SET info = '{}' WHERE `id` = '{}' ".format (session,635)
        print ('[sql]:',sql)
        cursor.execute(sql)
        db.commit()

        
#else:
	#print ('    [+] Удалите информации у базе данных или найдите нового клиента',lbl)