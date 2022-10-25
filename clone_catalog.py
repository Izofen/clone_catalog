# Версия 4.1. 
# Клонируем канал и фильтруем по сообщениям


import configparser
config = configparser.ConfigParser()
config.read('settings.ini') 
database = config.get('Settings', "database")
host     = config.get('Settings', "host")
user     = config.get('Settings', "user")
password = config.get('Settings', "password")
connect_info = {'host':host,'user':user,'password':password,'database':database}
api_id       = config.get('Settings', "api_id")
api_hash     = config.get('Settings', "api_hash")

def connect (connect_info):
    import pymysql 
    db = pymysql.connect(host=connect_info['host'],user=connect_info['user'],password=connect_info['password'],database=connect_info['database'],charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)  
    cursor = db.cursor() 
    return db,cursor

def telegram_connect (phone_number,api_id,api_hash):         ### Подлючение телеграмм клиента по имени учетки (телефон)
    if phone_number.find ('+') == -1:
        phone_number = '+'+str(phone_number)
    #print ('[+] phone_number:',phone_number)
    client = ''
    answer = 'Отсутствует учетная запись в базе'
    from telethon.sync import TelegramClient
    from telethon.sessions import StringSession
    db,cursor = connect (connect_info)
    sql = "select id,name,session from accound where name = '"+str(phone_number)+"' limit 1"
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data: 
        id,name,session = rec.values()
        client = TelegramClient(StringSession(session),api_id=api_id,api_hash=api_hash)
        client.connect()
        if not client.is_user_authorized():
            answer = 'Отсутствует подключение к телеграмм серверу'
        else:
            answer = 'Подключение к телеграмм серверу успешно'
    return client,answer

def save_message_send (answer,message_id,phone_number):
    sql = "INSERT INTO message_send (message,message_id,accound,unixtime,status) VALUES (%s,%s,%s,%s,%s)".format ()
    sql_save = (answer.stringify(),answer.id,phone_number,int(time.time()),'')
    cursor.execute(sql,sql_save)
    db.commit()    

def get_tasks (): 
    sql = "select id,name,data from task where 1=1".format ()
    cursor.execute(sql)
    results = cursor.fetchall()    
    return results

def get_message (client,name_dialog,depth):
    messages = client.iter_messages(name_dialog,depth)
    return messages 

def test_save_base (message_id,catalog_in,phone_number):
    id = 0
    sql = "select id from message_save where message_id = {} and catalog_in = '{}' and accound = '{}' limit 1".format (message_id,catalog_in,phone_number)
    cursor.execute(sql)
    results = cursor.fetchall()    
    for row in results:
        id = row['id']
    if id == 0:
        print ('        [+] Записиваем новое сообщение') 
        sql = "INSERT INTO message_save (message,message_id,accound,unixtime,catalog_in) VALUES (%s,%s,%s,%s,%s)".format ()
        sql_save = (message.stringify(),message_id,phone_number,int(time.time()),name_dialog)
        cursor.execute(sql,sql_save)
        db.commit()    
        
    return id    

def get_find_word (list_search):
    search_result = []
    for search in list_search:  
        print ('           [+] Поиск слова:',search,'Результат:',search_result)
        if message_text.find (search) != -1:
            search_result.append (search)
    return search_result        

def get_change_message (message,list_change):
    for change in list_change:                
        message.text = message.text.replace(change[0],change[1])
        hat = hat_shablon.replace('#data1#',str(search_result))
        message.text = hat+'\n'+message.text  
    return message    

def send_message_catalog (catalog_out,message):
    answer = client.send_message(catalog_out,message)
    return answer
    
while 1==1:    
    import json
    import time
    print ('[+] Программа для клонирования каталога.')
    db,cursor = connect (connect_info)    
    tasks = get_tasks ()
    for task in tasks:
        id,name,data = task.values() 
        print ('[+] data',data)
        parser_string = json.loads(data)
        #print ('[+] parser_string:',parser_string)
        command = parser_string.setdefault('command','error')
        if command == 'clone':
            print ('    [+] Выполнение клонирование каталога')    
            task        = parser_string.setdefault('task','')
            catalog_in  = task.setdefault('catalog_in' ,'')
            catalog_out = task.setdefault('catalog_out','')
            accound     = task.setdefault('accound','')
            change      = task.setdefault('change','')
            search      = task.setdefault('search','')
            depth       = task.setdefault('depth',100)
            wain        = task.setdefault('depth',10)
            hat_shablon = task.setdefault('hat_shablon','')
            print ('    [+] catalog_in:',catalog_in)
            print ('    [+] catalog_out:',catalog_out)
            print ('    [+] accound:',accound)
            print ('    [+] change:',change)
            print ('    [+] search:',search)
            from telethon import utils
            list_change  = change
            list_search  = search
            phone_number = accound.setdefault('name','')        
            api_id       = accound.setdefault('api_id'  ,api_id)
            api_hash     = accound.setdefault('api_hash',api_hash)
            name_dialog = catalog_in        
            client,answer = telegram_connect (phone_number,api_id,api_hash)
            messages =  get_message (client,name_dialog,depth)
            for message in messages:
                message_id      = message.id        
                message_text    = message.text
                message_text    = message_text.strip()
                id = test_save_base (message_id,catalog_in,phone_number)   
                if id == 0:
                    search_result = get_find_word (list_search)
                    if search_result != []:
                        print ('    [+] Отправка файлов')
                        print ('    [message_text]',message_text)
                        message = get_change_message (message,list_change)                    
                        answer = send_message_catalog (catalog_out,message)
                        answer_id = answer.id
                        print ('[+] answer:',answer_id)
                        print ('[+] answer:',answer)
                        save_message_send (answer,message_id,phone_number)
                        time.sleep (wain)
                else:
                    print ('[+] Пропускаем данную запись - обработана ранее')
            
    time.sleep (60*10)    
