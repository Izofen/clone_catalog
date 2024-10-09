# Версия 4.1. 
# Клонируем канал и фильтруем по сообщениям
import random

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
    
if 1==1:
    import optparse
    parser =  optparse.OptionParser(version='1.0',description='Шаблон')
    parser.add_option('-m','--menu', type='string', dest='menu', help='Меню')
    parser.add_option('-c','--city', type='string', dest='city', help='Город')
    parser.add_option('-i','--id', type='int', dest='id', help='id')
    (options, args) = parser.parse_args()
    ### --------------------------------------------------------------------------
    if options.menu == None:
        print ('[+] Укажите параметры запуска')


def connect (connect_info):
    import pymysql 
    db = pymysql.connect(host=connect_info['host'],user=connect_info['user'],password=connect_info['password'],database=connect_info['database'],charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)  
    cursor = db.cursor() 
    return db,cursor

def telegram_connect (phone_number,api_id,api_hash):         ### Подлючение телеграмм клиента по имени учетки (телефон)
    host = '127.0.0.1'       
    user = 'izofen'
    password = 'podkjf4'
    database = 'telegram'
    connect_info = {'host':host,'user':user,'password':password,'database':database} 
    db,cursor = connect (connect_info)      
    client = ''
    answer = 'Отсутствует учетная запись в базе'
    from telethon.sync import TelegramClient
    from telethon.sessions import StringSession    
    namebot = 'telegram'
    #db,cursor = iz_bot.connect (namebot)   
    sql = "select id,info from accound where name = 'Токен' and data_id = {} limit 1".format(phone_number)
    print ('sql',sql)
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data: 
        id,info = rec.values()
        session = info
        if str(phone_number) == str(634):
            session = '1ApWapzMBu6H7zrIzf7SRxg22aQJhk-MwX0vNkPu55_3513F_uPkoneABN40MrbHqtndo4pFBzEViB00oMKkg3Ky52-oF68bCjRlk-iyhrXG9tUXpqbgCTPRe4pa4M7xfB4Mu08xFoSwKJTDbJMyK0T7d-IbLy8LHIVew27tvBhxCxMyAaJBJQPJYtmsMbJmAT4wIxMEO0FCyXTr2rl7KyBFt1lVEmIjrUVl8J_FmxdjbI7JaMOWVKa-s_0gncyE0iwIu9TAUy9iIPANDl_mwZSJS65de5UzVz-7kPo0E05H2zjt3uFZvMtBuaWNh3C18dLs2xYFzn7P6vz-6kNJvThiO8kHwxH4='
            session = '1ApWapzMBu51Aobrln_ja5Nzgyr9oT5BLS_0Iqmi2EfZZuvmEiCa9h5sZVC1r84y74Zsdh0d3-dYSP4nydcIxd23EcYD4kqvbVBSqaL22jkw2gZaRohzZbyF3xTcNa0TTzLvEEQr5QCh73JKKdurp8T-i0DTeub-30qFsm55JaffMlp8cG_ANIfWjZJ35hr3TBAql4WX-zNEihOB4QuSGelpIiZSVu0rzkHvHXVAlqpiHfqfpI2UFUaIxqF64L9L9IDzpvZAiYEdjXVOfYRzPUA7GAzoF6OpijDj-pkXLh4A4L49h884IFaVP7NWKX2qs48nJv2tNvQxzh3G4Bkm7di2xdCqq5DQ='
            #print ('[session]',session)
            
            session = '1ApWapzMBu07SF8R5NXr1ElUqz9qvHOn4DYP1QK--UPTiqNHr4HONfsKe-WirlI1d5YlG2_v9DDDsx_-7Sb_jyCC8EVnZLwbyFvGjUR-KFyt5pbgSWqZxTv9t2ncC1ICs_QDZUMlTY_PV8VFadnKjnI3yOoIdLfR4nPWMeHb_EoJhfk7gmw9hxD2bbdaHEer9RvF5Ngmc46BPiQGa7yNp6zlGNMf0p-Sayo24u8jH5Yq2BidAtBAx5N5GGBt8icMQeupDS6PMVmVfbvukTUK1thqsQGiFh0orKegNkSnNbeXiwL3VhB8EgjemM8h_AeRi2LOhKTCWchXIodCIfJMiEaDZG17Uq5g='
            
            
        client = TelegramClient(StringSession(session),api_id=api_id,api_hash=api_hash)
        client.connect()
        if not client.is_user_authorized():
            answer = 'Отсутствует подключение к телеграмм серверу'
        else:
            answer = 'Подключение к телеграмм серверу успешно'
    db.close()           
    return client,answer
 
def get_client ():
    import iz_bot
    import random
    namebot = 'telegram'
    db,cursor = iz_bot.connect (namebot)   
    sql = "select id,info as name from accound where name = 'Имя' "
    cursor.execute(sql)
    data = cursor.fetchall()
    random.shuffle(data)
    db.close()   
    return data[0]

def save_message_send (answer,message_id,phone_number):
    namebot = 'telegram'
    #raw_text = message.raw_text
    db,cursor = iz_bot.connect (namebot)       
    sql = "INSERT INTO message_send (message,message_id,accound,unixtime,status) VALUES (%s,%s,%s,%s,%s)".format ()
    sql_save = (answer.stringify(),answer.id,str(phone_number),int(time.time()),'')
    cursor.execute(sql,sql_save)
    db.commit() 
    db.close()       

def get_tasks (name): 
    namebot = 'telegram'
    db,cursor = iz_bot.connect (namebot)       
    sql = "select id,name,`data` from task where status <> 'Delete' and name = '{}' ORDER BY unixtime limit 1 ".format (name)
    print ('[sql]',sql)
    cursor.execute(sql)
    results = cursor.fetchall()  
    db.close()       
    return results

def get_message (client,name_dialog,depth):
    messages = client.iter_messages(name_dialog,depth)
    return messages 

def test_save_base (message_id,catalog_in,phone_number,raw_text):
    namebot = 'telegram'
    db,cursor = iz_bot.connect (namebot)       
    id = 0
    sql = "select id from message_save where message_id = {} and catalog_in = '{}' limit 1".format (message_id,catalog_in,phone_number)
    cursor.execute(sql)
    results = cursor.fetchall()    
    for row in results:
        id = row['id']
    if id == 0:
        print ('        [+] Записиваем новое сообщение') 
        sql = "INSERT INTO message_save (message,message_id,accound,unixtime,catalog_in,`text`) VALUES (%s,%s,%s,%s,%s,%s)".format ()
        sql_save = (message.stringify(),message_id,str(phone_number),int(time.time()),name_dialog,str(raw_text))
        cursor.execute(sql,sql_save)
        db.commit()    
    db.close()    
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

def send_forward_catalog (client,catalog_out,message):
    #message.text = message.text.replace('**','')
    print ('[+] Отправка ------------------------------------------------------------------- [+]')
    if 1==1:
    #try:
        #answer = client.send_message(-1001846436203,message)
        answer = client.forward_messages(-1001846436203, message)
    #except:    
    #    answer = ''
    return answer
    
def send_message_catalog (client,catalog_out,message):
    #message.text = message.text.replace('**','')
    print ('[+] Отправка ------------------------------------------------------------------- [+]')
    if 1==1:
    #try:
        answer = client.send_message(-1001846436203,message)
        #answer = client.forward_messages(-1001846436203, message)
    #except:    
    #    answer = ''
    return answer        
    
def send_forward_catalog2 (client,catalog_out,message):
    #message.text = message.text.replace('**','')
    print ('[+] Отправка ------------------------------------------------------------------- [+]')
    if 1==1:
    #try:
        #answer = client.send_message(-1001846436203,message)
        answer = client.forward_messages(-664200845, message)
    #except:    
    #    answer = ''
    return answer    
    
def send_message_catalog2 (client,catalog_out,message):
    #message.text = message.text.replace('**','')
    print ('[+] Отправка ------------------------------------------------------------------- [+]')
    if 1==1:
    #try:
        answer = client.send_message(-664200845,message)
        #answer = client.forward_messages(-1001846436203, message)
    #except:    
    #    answer = ''
    return answer        
  
def set_print (title,setting,answer): 
    import datetime
    if answer == 'Main':        
        print ('[+]',title)   
        import iz_info       
        change =[['#Ответ#',str("Нет необходимый данных")],['#Режим#','Запуск в дневное время'],['#Пояснение#','Сбор данных с внешних групп']]
        iz_info.send_message ({'Имя':'Парсим информацию для Юристов','connect_info':{},'sql':'','Замена':change},setting)
  
def set_start (title,start_d,finish_d):  
    print ('[+] Проверка выполнения даты')
    import datetime
    now = datetime.datetime.now()
    print("[+]Hour : ",now.hour,start_d)
    if int(now.hour) < start_d:
        import time
        import iz_info
        print ('[+] Ожидаем начало работы ... (Юрист)')
        wait = (start_d - now.hour) * 60 * 60
        wait = wait - now.minute * 60
        wait = wait - now.second 
        change =[['#Режим#','Ожидаем запуск программы ... '],['#Пояснение#','Время ожидания:'+str(int(wait/60))+' мин.']]
        iz_info.send_message ({'Имя':'Парсим информацию для Юристов','Замена':change},'No')
        print ('    [+] Ожидаем начало запуска',wait,int(wait/60))    
        time.sleep (wait)
    
    if int(now.hour) > finish_d:   
        import time 
        import iz_info        
        print ('[+] Ожидаем начало работы ... (Юрист)')
        wait = (24 - now.hour) * 60 * 60        
        wait = wait - now.minute * 60
        wait = wait - now.second
        wait = wait + start_d * 60 * 60
        change =[['#Режим#','Ожидаем запуск программы ... '],['#Пояснение#','Время ожидания:'+str(int(wait/60))+' мин.']]
        iz_info.send_message ({'Имя':'Парсим информацию для Юристов','Замена':change},'No')
        print ('    [+] Ожидаем начало запуска',wait,int(wait/60))    
        time.sleep (wait)
  
  
def setting (remark):
    answer = {}
    connect_info = {'host':'localhost','user':'izofen','password':'podkjf4','database':'telegram'} 
    db,cursor = connect (connect_info)  
    sql = "select id,name,result from setting where remark = '{}' ".format (remark) 
    cursor.execute(sql)
    results = cursor.fetchall()    
    for row in results:
        id,name,result = row.values() 
        answer[name] = result
    return answer  
  
  
if options.menu == None:
    print ('   [+] 1 - Запуск программы - coube 1')
    print ('   [+] 2 - Программа для клонирования каталога')
    print ('   [+] 3 - Копируем информацию в ВК')
    print ('   [+] 5 - Перенос всей информации из одного калалога в другой')

if options.menu == '1':
    import datetime
    now = datetime.datetime.now()
    time_send = now.strftime("%d-%m-%Y %H:%M")
    print ('[+] ------------------------------------------------ Запуск программы - coube 1',time_send),'------------------------------------------------'
    import json
    import time
    import iz_info
    import iz_bot
    connect_info = {'host':host,'user':user,'password':password,'database':'coube'}
    db,cursor = connect (connect_info)    
    sql = "select id,name from coube_name where status <> 'send' limit 1".format ()
    cursor.execute(sql)
    results = cursor.fetchall()  
    name = ''
    for row in results:
        id,name = row.values() 
        print ('[+] id,name',id,name)
    list_phone_number = [{'name':'+79033671563','id':369}]
    list_phone_number = [{'name':'+79162254209','id':463}]
    random.shuffle(list_phone_number) 
    phone_number = list_phone_number[0]
    print ('[phone_number]',phone_number)
    setting  = iz_bot.get_setting ({'namebot':'@info314_bot'})
    api_id   = int(setting.setdefault('api_id',0))      #192804
    api_hash = str(setting.setdefault('api_hash',''))   #'1b40d1d01f8922b384d44e29d32f6acf'
    print ('[+] Настройки клиента',api_id,api_hash)
    client,answer = telegram_connect (phone_number,api_id,api_hash)
    #catalog_out = -1001881718003
    catalog_out = 'https://t.me/coube314'   ## Coube в телеграмм
    if name != '':
        message     = name
        answer  = send_message_catalog (client,catalog_out,message)
        print ('[+] Ответ публикации:',answer)
        connect_info = {'host':host,'user':user,'password':password,'database':'coube'}
        db,cursor = connect (connect_info)  
        sql = "UPDATE coube_name SET status = '{}' WHERE `id` = '{}' ".format ("send",id)
        cursor.execute(sql)
        db.commit()
        change = []
        change.append (['#Ответ#',str(str(name))])    
        sql = "SELECT COUNT(*) FROM coube_name WHERE status = '' "
        iz_info.send_message ({'Имя':'Старт запуска Coube','connect_info':connect_info,'sql':sql,'Замена':change})
    else:    
        change = []
        change.append (['#Ответ#',str("Нет необходимый данных")])    
        sql = "SELECT COUNT(*) FROM coube_name WHERE status = '' "
        iz_info.send_message ({'Имя':'Старт запуска Coube','connect_info':connect_info,'sql':sql,'Замена':change})
    db.close()       
           
if options.menu == '2': 
    print ('Программа для кланирования телеграмм информации')
    import iz_info
    import iz_bot
    host = '127.0.0.1'       
    user = 'root'
    password = 'Podkjf3141'
    database = 'telegram'
    connect_info = {'host':host,'user':user,'password':password,'database':database}  

if options.menu == '3':   
    print ('[+] Копируем информацию в ВК')
    import json
    import time
    import requests
    import iz_info
    import iz_bot
    setting = iz_bot.get_setting ({'namebot':'@info314_bot'})
    change = []
    change.append (['#Ответ#',str("Нет необходимый данных")])    
    #sql = "SELECT COUNT(*) FROM coube_name WHERE status = '' "
    iz_info.send_message ({'Имя':'Запуск пополнения ВК групп','connect_info':connect_info,'sql':'','Замена':change})    
    api_id   = int(setting.setdefault('api_id',0))      #192804
    api_hash = str(setting.setdefault('api_hash',''))   #'1b40d1d01f8922b384d44e29d32f6acf'
    
    host = '127.0.0.1'       
    user = 'root'
    password = 'Podkjf3141'
    database = 'telegram'
    
    connect_info = {'host':host,'user':user,'password':password,'database':database}  
    if 1==1:
        import json
        import time
        print ('[+] Программа для клонирования каталога.')
        print ('[connect_info]',connect_info)
        db,cursor = connect (connect_info)    
        tasks = get_tasks ('clone_vk')
        for task in tasks:
            id_task,name,data = task.values() 
            print ('[+] data',data)
            parser_string = json.loads(data)            
            #list_phone_number = ['+79033671563']
            #random.shuffle(list_phone_number) 
            #phone_number = list_phone_number[0]
            #print ('[phone_number]',phone_number)
            #client,answer = telegram_connect (phone_number,api_id,api_hash)
            answer = 'Отсутствует подключение к телеграмм серверу'
            while answer == 'Отсутствует подключение к телеграмм серверу':
                phone_number = get_client ()
                print ('    [+],phone_number',phone_number)
                client,answer = telegram_connect (phone_number,api_id,api_hash)
                print ('[answer]',answer)
                time.sleep (3)
            task_p = parser_string.setdefault('task','')
            print ('[+] task_p',task_p)
            catalog_in  = task_p.setdefault('catalog_in' ,'')
            catalog_out = task_p.setdefault('catalog_out','')
            accound     = task_p.setdefault('accound','')  
            token       = task_p.setdefault('token','')  
            ### 'vk1.a.VSQxiNXpo7SkKi89s6R3guDVSsKKBLT-WSfW1qVbZOh8QgmbEgmPmBOg581C7-H6eGIVMt_g84jd-63GufOogFjiyc5xSH4-EgRJztkIgvaynzvZyVR1zkwXImUyomAHU05s30EJwF4GJpA81y178HNjCg6eWLh_Zt8lxpyCdXyupKpSs7MUICZRMI8xs4fBjL_fO4snLPzkW3ir4ZX-Lw'
            print ('[+] catalog_in',catalog_in)
            name_dialog = catalog_in        
            print ('[+] name_dialog',name_dialog)
            messages =  get_message (client,name_dialog,10)
            print ('[messages]',messages)
            for message in messages:
                message_id      = message.id        
                message_text    = message.text
                print ('    [+] --------------------------------------------------------------------- [+]')
                print ('    [+] ',message_id)               
                message_text    = str(message_text).strip()
                raw_text        = message.raw_text
                id = test_save_base (message_id,catalog_in,phone_number,raw_text) 
                print ('        [+] id нашей базы:',id)
                if id == 0:
                    print ('    [+] ',message_text)
                    change = []
                    change.append (['#Ответ#',str(message_text)])    
                    #sql = "SELECT COUNT(*) FROM coube_name WHERE status = '' "
                    iz_info.send_message ({'Имя':'Новая публикация в ВК групп','connect_info':connect_info,'sql':'','Замена':change})    
                    import requests
                    owner_id_group = catalog_out
                    data = {'access_token': token,'v':5.131,'message':message_text,'owner_id':owner_id_group}          ### 'owner_id': owner_id_group,'from_group': 1,'message': message_text,'signed': 0,'v':"5.52"
                    answer = requests.post('https://api.vk.com/method/wall.post', data=data).json()
                    print (answer)
                print ('    [+] ')  
            sql = "UPDATE task SET unixtime = {} WHERE `id` = {} ".format (int(time.time()),id_task)
            cursor.execute(sql)
            db.commit() 
    db.close()               
   
if options.menu == '4': 
    print ('[+] Перенос аккаунтов из базы')
    import iz_bot
    namebot = 'main'
    db_main,cursor_main = iz_bot.connect (namebot)   
    if 1==1:  # Клонируем
        namebot = 'telegram'
        db,cursor = iz_bot.connect (namebot)
        sql_main = "select id,name,session from telegram_session where 1=1;"
        cursor_main.execute(sql_main)
        data_main = cursor_main.fetchall()
        for rec_main in data_main: 
            id_main,name_main,session_main = rec_main.values()
            print ('    [+] name_main',name_main)
            sql = "select id,name from accound where name = 'Имя' and info = '{}';".format(name_main)
            id = 0
            cursor.execute(sql)
            data = cursor.fetchall()
            for rec in data: 
                id,name = rec.values()
            if id == 0:
                print ('        [+] Создем новый аккаунд') 
                sql = "INSERT INTO accound (name,data_id,info,status) VALUES (%s,%s,%s,%s)".format ()
                sql_save = ('Имя',0,name_main,'')
                cursor.execute(sql,sql_save)
                lastid = cursor.lastrowid
                sql = "UPDATE accound SET data_id = {} WHERE id = {}".format(lastid,lastid)
                cursor.execute(sql)
                db.commit()           
                sql = "INSERT INTO accound (name,data_id,info,status) VALUES (%s,%s,%s,%s)".format ()
                sql_save = ('Токен',lastid,session_main,'')
                cursor.execute(sql,sql_save)            
                db.commit() 
            else:
                print ('   [+] Пропускаем ')    

    if 1==1:  # Ping база
        namebot = 'ping314_bot'
        db,cursor = iz_bot.connect (namebot)
        sql_main = "select id,name,session from telegram_session where 1=1;"
        cursor_main.execute(sql_main)
        data_main = cursor_main.fetchall()
        for rec_main in data_main: 
            id_main,name_main,session_main = rec_main.values()
            print ('    [+] name_main',name_main)
            sql = "select id,name from accound where name = 'Имя' and info = '{}';".format(name_main)
            id = 0
            cursor.execute(sql)
            data = cursor.fetchall()
            for rec in data: 
                id,name = rec.values()
            if id == 0:
                print ('        [+] Создем новый аккаунд') 
                sql = "INSERT INTO accound (name,data_id,info,status) VALUES (%s,%s,%s,%s)".format ()
                sql_save = ('Имя',0,name_main,'')
                cursor.execute(sql,sql_save)
                lastid = cursor.lastrowid
                sql = "UPDATE accound SET data_id = {} WHERE id = {}".format(lastid,lastid)
                cursor.execute(sql)
                db.commit()           
                sql = "INSERT INTO accound (name,data_id,info,status) VALUES (%s,%s,%s,%s)".format ()
                sql_save = ('Токен',lastid,session_main,'')
                cursor.execute(sql,sql_save)            
                db.commit()                   
    db.close()       
        
if options.menu == '5': 
    import iz_info
    import json
    import time
    import iz_bot
    host = '127.0.0.1'       
    user = 'root'
    password = 'Podkjf3141'
    database = 'telegram'
    connect_info = {'host':host,'user':user,'password':password,'database':database}  
    setting = iz_bot.get_setting ({'namebot':'@info314_bot'})    
    print ('[+] Программа для клонирования каталога.')
    db,cursor = connect (connect_info)    
    tasks = get_tasks ('copy')
    for task in tasks:
        if 1==1:
            id_task,name,data = task.values() 
            print ('[+] id_task',id_task,data)
            parser_string = json.loads(data)
            #print ('[+] parser_string:',parser_string)
            command = parser_string.setdefault('command','error')
            if command == 'copy':
                print ('    [+] Копирование каталога')    
                task        = parser_string.setdefault('task','')
                catalog_in  = task.setdefault('catalog_in' ,'')
                print ('   [+] Читаем данные из каталога:',catalog_in)
                time.sleep (3)
                catalog_out = task.setdefault('catalog_out','')
                accound     = task.setdefault('accound',{})
                change      = task.setdefault('change','')
                search      = task.setdefault('search','')
                depth       = task.setdefault('depth',10)
                wait        = task.setdefault('wait',10)
                hat_shablon = task.setdefault('hat_shablon','')
                print ('    [+] catalog_in:',catalog_in)
                print ('    [+] catalog_out:',catalog_out)
                print ('    [+] accound:',accound)
                print ('    [+] change:',change)
                print ('    [+] search:',search)
                from telethon import utils
                list_change  = change
                list_search  = search
                api_id       = accound.setdefault('api_id'  ,api_id)
                api_hash     = accound.setdefault('api_hash',api_hash)
                answer = 'Отсутствует подключение к телеграмм серверу'
                while answer == 'Отсутствует подключение к телеграмм серверу':
                    phone_number = get_client ()
                    print ('    [+],phone_number',phone_number)
                    client,answer = telegram_connect (phone_number,api_id,api_hash)
                    print ('[answer]',answer)
                    time.sleep (3)
                name_dialog = catalog_in        
                messages =  get_message (client,name_dialog,depth)
                print ('[messages]',messages)
                #exit (0)
                #print ('[messages]',messages)
                for message in messages:
                    message_id      = message.id        
                    message_text    = message.text
                    raw_text        = message.raw_text
                    print ('    [+] -- 1 ------------------------------------------------------------------- [+]')
                    print ('    [+] ',message_id)
                    print ('    [+] ',message_text)
                    #print ('    [+] ')
                    message_text    = str(message_text).strip()
                    id = test_save_base (message_id,catalog_in,phone_number,raw_text)   
                    if id == 0:
                        catalog_out = -1001881718003
                        #message = 'TEST 2'
                        list_phone_number = [{'name':'+79033671563','id':369}]
                        #list_phone_number = [{'name':'+79162254209','id':463}]
                        random.shuffle(list_phone_number) 
                        phone_number = list_phone_number[0]
                        #print ('[phone_number]',phone_number)
                        setting  = iz_bot.get_setting ({'namebot':'@info314_bot'})
                        api_id   = int(setting.setdefault('api_id',192804))      #192804
                        api_hash = str(setting.setdefault('api_hash','1b40d1d01f8922b384d44e29d32f6acf'))   #'1b40d1d01f8922b384d44e29d32f6acf'
                        #print ('[+] Настройки клиента',api_id,api_hash)
                        #print ('----------------------------------------------------------------------')
                        client_79033671563,answer = telegram_connect (phone_number,api_id,api_hash) 
                        answer  = send_message_catalog (client_79033671563,catalog_out,message)
                        print ('[+] answer',answer)
                        print ('    [message_text]',message_text)        
                #            if answer != '':
                #                answer_id = answer.id
                #                print ('[+] answer:',answer_id)
                #                print ('[+] answer:',answer)
                #                save_message_send (answer,message_id,phone_number)
                #            else:
                #               print ('[+] Ошибка записи')
                #                iz_info.send_message ({'Имя':'Ошибка отправки сообщения Job','Замена':change})
                
                        print ('wait ',wait)
                        time.sleep (wait)
                
                    else:
                        print ('        [+] Пропускаем данную запись - обработана ранее')
                        pass
                    print ('    [+] --------------------------------------------------------------------- [+]')
                    time_wait = int(setting.setdefault('Job Время между заданиями',1)) #192804
                    print ('[+] Ожидаем',time_wait,'сек.')
                    time.sleep (time_wait)
            namebot = 'telegram'
            db,cursor = iz_bot.connect (namebot)       
            sql = "UPDATE task SET unixtime = {} WHERE `id` = {} ".format (int(time.time()),id_task)
            cursor.execute(sql)
            db.commit()            
    db.close()   
  
if options.menu == '6': 
    import iz_bot        
    accound      = {}        
    api_id       = accound.setdefault('api_id'  ,api_id)
    api_hash     = accound.setdefault('api_hash',api_hash)
    #list_phone_number = [{'name':'+79033671563','id':369}]
    #list_phone_number = [{'name':'+79162254209','id':463}]
    #random.shuffle(list_phone_number) 
    #phone_number = list_phone_number[0]
    phone_number = 634
    client,answer = telegram_connect (phone_number,api_id,api_hash)
    print (answer)
    #list = []
    for dialog in client.iter_dialogs():
    #    #print (dialog)
        print(dialog.name, 'has ID', dialog.id)
 
if options.menu == '7':
    import iz_bot   
    catalog_out = -1001881718003
    message = 'TEST'
    list_phone_number = [{'name':'+79033671563','id':369}]
    #list_phone_number = [{'name':'+79162254209','id':463}]
    random.shuffle(list_phone_number) 
    phone_number = list_phone_number[0]
    print ('[phone_number]',phone_number)
    setting  = iz_bot.get_setting ({'namebot':'@info314_bot'})
    api_id   = int(setting.setdefault('api_id',192804))      #192804
    api_hash = str(setting.setdefault('api_hash','1b40d1d01f8922b384d44e29d32f6acf'))   #'1b40d1d01f8922b384d44e29d32f6acf'
    print ('[+] Настройки клиента',api_id,api_hash)
    print ('----------------------------------------------------------------------')
    client_79033671563,answer = telegram_connect (phone_number,api_id,api_hash) 
    answer  = send_message_catalog (client_79033671563,catalog_out,message)
    print ('[+] answer',answer)
 
if options.menu == '8':
    print ("Публикуем новости на время")    
    import requests
    method = "sendMessage"
    token   = "5713227819:AAGE5XdsgHs_YHNaOpwcxHXLT9pL9Hkpvok"
    user_id = "coube314"
    message = "test"
    params = {}
    params['chat_id']   = user_id   ##"399838806"                
    params['text']      = message
    params['parse_mode'] = 'HTML'
    url  = 'https://api.telegram.org/bot{0}/{1}'.format(token, method)
    resp = requests.post(url, params)     
    print ('[resp]',resp.text)

if options.menu == '9':
    import iz_bot   
    catalog_out = -1001881718003
    message = 'TEST'
    list_phone_number = [{'name':'+79033671563','id':369}]
    #list_phone_number = [{'name':'+79162254209','id':463}]
    random.shuffle(list_phone_number) 
    phone_number = list_phone_number[0]
    print ('[phone_number]',phone_number)
    setting  = iz_bot.get_setting ({'namebot':'@info314_bot'})
    api_id   = int(setting.setdefault('api_id',192804))      #192804
    api_hash = str(setting.setdefault('api_hash','1b40d1d01f8922b384d44e29d32f6acf'))   #'1b40d1d01f8922b384d44e29d32f6acf'
    print ('[+] Настройки клиента',api_id,api_hash)
    print ('----------------------------------------------------------------------')
    client_79033671563,answer = telegram_connect (phone_number,api_id,api_hash) 
    #answer  = send_message_catalog (client_79033671563,catalog_out,message)
    answer  = client_79033671563.get_entity('https://t.me/main314_bot')
    print ('[+] answer',answer)
    print ('[+] answer',answer.bot)
    answer  = client_79033671563.get_entity('https://t.me/coube314')
    print ('[+] answer',answer)
    print ('[+] answer',answer.title)
    #print ('[+] answer',answer.bot)
    answer  = client_79033671563.get_entity('https://t.me/bot3dot14')
    print ('[+] answer',answer)
    print ('[+] answer',answer.title)

if options.menu == '10':
    import iz_bot
    catalog_out = -1001223464987  #### nnmclub
    message     = 'TEST2'
    #from telethon.tl.functions.messages import AddChatUserRequest
    #from telethon.tl.functions.channels import InviteToChannelRequest
    from telethon import functions, types
    list_phone_number = [{'name':'+79033671563','id':369}]
    #list_phone_number = [{'name':'+79162254209','id':463}]
    random.shuffle(list_phone_number) 
    phone_number = list_phone_number[0]
    print ('[phone_number]',phone_number)
    setting  = iz_bot.get_setting ({'namebot':'@info314_bot'})
    api_id   = int(setting.setdefault('api_id',192804))      #192804
    api_hash = str(setting.setdefault('api_hash','1b40d1d01f8922b384d44e29d32f6acf'))   #'1b40d1d01f8922b384d44e29d32f6acf'
    print ('[+] Настройки клиента',api_id,api_hash)
    print ('----------------------------------------------------------------------')
    client_79033671563,answer = telegram_connect (phone_number,api_id,api_hash) 
    result = client_79033671563(functions.channels.InviteToChannelRequest(channel='https://t.me/nnm_club314',users=['master11111111111221']))
    print ('[+] answer',answer)

if options.menu == '11':
    print ('[+] Информация о клиенте')
    import iz_bot
    #catalog_out = -1001223464987  #### nnmclub
    #message     = 'TEST2'
    #from telethon.tl.functions.messages import AddChatUserRequest
    #from telethon.tl.functions.channels import InviteToChannelRequest
    from telethon import functions, types
    list_phone_number = [{'name':'+79033671563','id':369}]
    #list_phone_number = [{'name':'+79162254209','id':463}]
    random.shuffle(list_phone_number) 
    phone_number = list_phone_number[0]
    print ('[phone_number]',phone_number)
    setting  = iz_bot.get_setting ({'namebot':'@info314_bot'})
    api_id   = int(setting.setdefault('api_id',192804))      #192804
    api_hash = str(setting.setdefault('api_hash','1b40d1d01f8922b384d44e29d32f6acf'))   #'1b40d1d01f8922b384d44e29d32f6acf'
    #print ('[+] Настройки клиента',api_id,api_hash)
    print ('----------------------------------------------------------------------')
    client_79033671563,answer = telegram_connect (phone_number,api_id,api_hash) 
    #result = client_79033671563(functions.channels.InviteToChannelRequest(channel='https://t.me/nnm_club314',users=['master11111111111221']))    
    answer  = client_79033671563.get_entity('EVOLUTION_TOP')
    #print ('[+] answer:',answer)    
    print ('[+] answer',answer)
 
if options.menu == '12':
    import pymysql 
    import random
    import time
    
    file1 = open("stoma_franch.txt", "r")
    lines = file1.readlines()
    users = []
    for line in lines:
        print(line.strip())
        users.append(line.strip()) 
    file1.close
    
    random.shuffle(users)
    #users = ['@evolution_top','@reactor_lead','@roman_reactor']
    base = 'main'
    db = pymysql.connect(host='192.168.1.120',user='root',password='Podkjf3141',database=base,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)        
    cursor = db.cursor()
    for user in users:
        print ('    [+] 1 user:',user)
        id_user = 0
        sql = "select id,name from telegram_send where name = '{}';".format (user)
        cursor.execute(sql)
        results = cursor.fetchall()  
        for row in results:  
            id_user,name_user = row.values()               
        if id_user == 0:
            sql = "select id,name,session from telegram_session where name like '+44%' and name <> '+447425061135' and status = '' ".format ()
            cursor.execute(sql)
            results = cursor.fetchall()  
            name = ''
            id,name,session = random.choice(results).values()
            #for row in results:
            print ('    [+] client:',id,name)        
            import iz_bot
            from telethon import functions, types
            #list_phone_number = [{'name':'+79033671563','id':369}]
            #random.shuffle(list_phone_number) 
            #phone_number = list_phone_number[0]
        
            #print ('[phone_number]',phone_number)
    
            setting  = iz_bot.get_setting ({'namebot':'@info314_bot'})
            api_id   = int(setting.setdefault('api_id',192804))      #192804
            api_hash = str(setting.setdefault('api_hash','1b40d1d01f8922b384d44e29d32f6acf'))   #'1b40d1d01f8922b384d44e29d32f6acf'
            #print ('----------------------------------------------------------------------')
    
            #client,answer = telegram_connect (phone_number,api_id,api_hash) 
    
            client = ''
            from telethon.sync import TelegramClient
            from telethon.sessions import StringSession    
        
            #session = info

            #print ('[session]',session)
    
            client = TelegramClient(StringSession(session),api_id=api_id,api_hash=api_hash)
            client.connect()
            if not client.is_user_authorized():
                answer = 'Отсутствует подключение к телеграмм серверу'
            else:
                answer = 'Подключение к телеграмм серверу успешно'    

            #answer  = client_79033671563.get_entity('EVOLUTION_TOP')
            #print ('[+] answer',answer)
    
            name_dialog = "https://t.me/info314"
            messages = client.iter_messages(name_dialog,1)
    
            for message in messages:
                message_id      = message.id        
                message_text    = message.text
                #print (message_text)
                #message.text = message.text.replace('#name#',"11111111111")
                
            #user = '@evolution_top'
        
            #user = line
            #print ('----------------------------------------------------------------------')
            print ('    [+] 2 user:',user)
            #print ('----------------------------------------------------------------------')
            first_name = ''
            try:
                in_user  = client.get_entity(user)
                first_name = in_user.first_name
                print ('[+] first_name:',first_name)
            except: 
                pass        
                sql = "INSERT INTO telegram_send (name,progect,status) VALUES (%s,%s,%s)".format ()
                sql_save = (user,'stomat','no find')
                cursor.execute(sql,sql_save)
                db.commit() 

            message.text = message.text.replace('#name#',str(first_name))
            #print ('----------------------------------------------------------------------')
            #print (message.text)
            #print ('----------------------------------------------------------------------')
        
            if first_name != '':
                try:
                    answer = client.send_message(user,message)
                    print ('[+] answer',answer)            
                    sql = "UPDATE telegram_session SET status = '{}' WHERE id = {} ".format ('good',id)
                    cursor.execute(sql)
                    db.commit()
                    sql = "INSERT INTO telegram_send (name,progect,status) VALUES (%s,%s,%s)".format ()
                    sql_save = (user,'stomat','send')
                    cursor.execute(sql,sql_save)
                    db.commit() 
                except:    
                    pass
                    sql = "UPDATE telegram_session SET status = '{}' WHERE id = {} ".format ('error',id)
                    cursor.execute(sql)
                    db.commit()
                print ('----------------------------------------------------------------------')   
            print ('[+] Пауза')        
            time.sleep (60*3)
        else:
            print ('[+] Сообщение было отправлено ранее ...')
    db.close()   

if options.menu == '13':
    print ("    [+] Проверяю активность телеграмм")
    #import iz_func
    import json
    import iz_bot
    import requests
    import time
    import random
    import pymysql
    db = pymysql.connect(host='localhost',
                            user='izofen',
                            password='podkjf4',
                            database='telegram',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)    
    cursor   = db.cursor()    

    sql = "select id,name,data_id,info from accound where name = 'Имя';"
    cursor.execute(sql)
    data = cursor.fetchall()
    list = []

    setting  = iz_bot.get_setting ({'namebot':'@info314_bot'})
    api_id   = int(setting.setdefault('api_id',192804))      #192804
    api_hash = str(setting.setdefault('api_hash','1b40d1d01f8922b384d44e29d32f6acf'))   #'1b40d1d01f8922b384d44e29d32f6acf'
    print ('[+] Настройки клиента',api_id,api_hash)
     
   
     
    for rec in data: 
        id,name,data_id,info = rec.values() 
        print ('[+]',id,name,data_id,info)
        id_k = 0 
        element = {}    
        sql = "select id,name,info from accound where data_id = {};".format (data_id)  
        cursor.execute(sql)
        data = cursor.fetchall()
        for rec in data: 
            id,name,info = rec.values()
            element[name] = info   
        print (element) 

        
        phone_number  = str(data_id)
        print ('[+] phone_number:',phone_number)
        client,answer = telegram_connect (phone_number,api_id,api_hash)
        print (client,answer)
        
        if answer == 'Отсутствует подключение к телеграмм серверу':
            name      = 'Ответ'
            data_id   = data_id
            info      = str('Отсутствует подключение к телеграмм серверу')
            status    = ''
            print(info)
        else:        
            me = client.get_me()
            name      = 'Ответ'
            data_id   = data_id
            info      = str(me.stringify())
            status    = ''
            print(info)
        
        
        sql = "INSERT INTO accound (`name`,`data_id`,`info`,`status`) VALUES (%s,%s,%s,%s)".format () 
        sql_save = (name,data_id,info,status)
        cursor.execute(sql,sql_save)
        lastid = cursor.lastrowid   
        db.commit() 
        
        time.sleep (10)
 
if options.menu == '23': 
    print ('Программа для клонирования телеграмм юристов 2')
    setting = {'namebot':'nnmclub314_bot'}    
    set_print ('Программа для клонирования телеграмм юристов',setting,'Main')    
    import iz_bot  
    import time     
    time.sleep (600)   
    host = '127.0.0.1'       
    user = 'izofen'
    password = 'podkjf4'
    database = 'law_help_bot'
    connect_info = {'host':host,'user':user,'password':password,'database':database} 
    setting = iz_bot.get_setting ({'namebot':'@law_help_bot'})  
    api_id   = int(setting.setdefault('api_id',192804))      #192804
    api_hash = str(setting.setdefault('api_hash','1b40d1d01f8922b384d44e29d32f6acf'))   #'1b40d1d01f8922b384d44e29d32f6acf'
    db,cursor = connect (connect_info)  
    sql = "select id,info from service where name = 'Слово 2'"
    cursor.execute(sql)
    data = cursor.fetchall()
    list = []
    for rec in data: 
        id,info = rec.values()
        list.append (info)
        print ('    [+]:',id,info)

    phone_number = 634
    client,answer = telegram_connect (phone_number,api_id,api_hash)
    print ('[+] answer:',answer)

    sql = "select id,info from service where name = 'Группа 2'"
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data: 
        id,info = rec.values()       
        name_dialog = info
        print ('    [+] Группа: ',name_dialog)
        depth       = 10
        messages =  get_message (client,name_dialog,depth)
        time.sleep (10)
        for message in messages:
            message_id      = message.id        
            message_text    = message.text
            print ('        [+] Новость: ',message_id)
            message_text    = str(message_text).strip()
                       
            sql = "select t1.id,t1.name from task as t1, task as t2 where t1.data_id = t2.data_id and t1.name = 'Задание 2' and t1.info = '"+str(message.id)+"' and t2.name = 'Группа' and t2.info = '"+str(name_dialog)+"'"
            cursor.execute(sql)
            data = cursor.fetchall()
            id = 0
            for rec in data: 
                id,name = rec.values() 

            if id == 0:
                        
                sql = "INSERT INTO task (`name`,`data_id`,`info`,`status`) VALUES ('Задание 2',0,'{}','')".format (str(message_id))
                cursor.execute(sql)
                db.commit()  
                lastid = cursor.lastrowid
                
                sql = "UPDATE task SET data_id = {} WHERE id = {} ".format (lastid,lastid)
                cursor.execute(sql)
                db.commit() 
            
                sql = "INSERT INTO task (`name`,`data_id`,`info`,`status`) VALUES ('Группа',{},'{}','')".format (lastid,name_dialog)
                cursor.execute(sql)
                db.commit()  
            
                sql = "INSERT INTO task (`name`,`data_id`,`info`,`status`) VALUES ('Статус',{},'{}','')".format (lastid,"Записан")
                cursor.execute(sql)
                db.commit()  
            
                sql = "INSERT INTO task (`name`,`data_id`,`info`,`status`) VALUES (%s,%s,%s,%s)".format ()
                sql_save = ('Текст',lastid,message_text,'')
                cursor.execute(sql,sql_save)
                db.commit()  
                        
                word_search = ""
                for line in list:
                    print ('             [+] Поиск слова:',line)
                    if message_text.find (line) != -1:
                        word_search = word_search + ", " + str(line)
                
                if word_search != '':
                    answer  = send_forward_catalog2 (client,'-664200845',message) 
                    answer  = send_message_catalog2 (client,'-664200845',str(word_search))   
                    time.sleep (60)
                    sql = "UPDATE task SET status = '{}' WHERE id = {} ".format ('Отправлен',lastid)
                    cursor.execute(sql)
                    db.commit()
                    sql = "INSERT INTO task (`name`,`data_id`,`info`,`status`) VALUES (%s,%s,%s,%s)".format ()
                    sql_save = ('Ответ',lastid,message_text,'')
                    cursor.execute(sql,sql_save)
                    db.commit()       
                    time.sleep (5)
                else:
                    sql = "UPDATE task SET info = '{}' WHERE data_id = {} and name = 'Статус' ".format ('Пропуск',lastid)
                    cursor.execute(sql)
                    db.commit() 
            
            else:
                print ('            [+] Пропуск новостей т.к. уже былы')
            #exit(0)
    
    time.sleep (600)        
             
if options.menu == '22': 
    print ('Программа для клонирования телеграмм юристов')
    setting = {'namebot':'nnmclub314_bot'}    
    set_print ('Программа для клонирования телеграмм юристов',setting,'Main')   
    set_start ('Днем',5,24)     
    import iz_bot  
    import time    
    host = '127.0.0.1'       
    user = 'izofen'
    password = 'podkjf4'
    database = 'law_help_bot'
    connect_info = {'host':host,'user':user,'password':password,'database':database} 
    setting = iz_bot.get_setting ({'namebot':'@law_help_bot'})  
    api_id   = int(setting.setdefault('api_id',192804))      #192804
    api_hash = str(setting.setdefault('api_hash','1b40d1d01f8922b384d44e29d32f6acf'))   #'1b40d1d01f8922b384d44e29d32f6acf'
    db,cursor = connect (connect_info)  
    sql = "select id,info from service where name = 'Слово'"
    cursor.execute(sql)
    data = cursor.fetchall()
    list = []
    for rec in data: 
        id,info = rec.values()
        list.append (info)
    phone_number = 634
    client,answer = telegram_connect (phone_number,api_id,api_hash)
    print ('[+] answer:',answer)
    sql = "select id,info from service where name = 'Группа'"
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data: 
        id,info = rec.values()       
        name_dialog = info
        print ('    [+] Группа: ',name_dialog)
        depth       = 10
        messages =  get_message (client,name_dialog,depth)
        #print (messages)
        time.sleep (10)
        for message in messages:
            message_id      = message.id        
            message_text    = message.text
            print ('        [+] Новость: ',message_id)
            message_text    = str(message_text).strip()            
            sql = "select t1.id,t1.name from task as t1, task as t2 where t1.data_id = t2.data_id and t1.name = 'Задание' and t1.info = '"+str(message.id)+"' and t2.name = 'Группа' and t2.info = '"+str(name_dialog)+"'"
            cursor.execute(sql)
            data = cursor.fetchall()
            id = 0
            for rec in data: 
                id,name = rec.values() 
            if id == 0:                      
                sql = "INSERT INTO task (`name`,`data_id`,`info`,`status`) VALUES ('Задание',0,'{}','')".format (str(message_id))
                cursor.execute(sql)
                db.commit()  
                lastid = cursor.lastrowid
                sql = "UPDATE task SET data_id = {} WHERE id = {} ".format (lastid,lastid)
                cursor.execute(sql)
                db.commit() 
                sql = "INSERT INTO task (`name`,`data_id`,`info`,`status`) VALUES ('Группа',{},'{}','')".format (lastid,name_dialog)
                cursor.execute(sql)
                db.commit()  
                sql = "INSERT INTO task (`name`,`data_id`,`info`,`status`) VALUES ('Статус',{},'{}','')".format (lastid,"Записан")
                cursor.execute(sql)
                db.commit()  
                sql = "INSERT INTO task (`name`,`data_id`,`info`,`status`) VALUES (%s,%s,%s,%s)".format ()
                sql_save = ('Текст',lastid,message_text,'')
                cursor.execute(sql,sql_save)
                db.commit()          
                word_search = ""
                for line in list:
                    print ('             [+] Поиск слова:',line)
                    if message_text.find (line) != -1:
                        word_search = word_search + ", " + str(line)
                if word_search != '':
                    answer  = send_forward_catalog (client,'-1001846436203',message) 
                    answer  = send_message_catalog (client,'-1001846436203',str(word_search))   
                    time.sleep (60)
                    sql = "UPDATE task SET status = '{}' WHERE id = {} ".format ('Отправлен',lastid)
                    cursor.execute(sql)
                    db.commit()
                    sql = "INSERT INTO task (`name`,`data_id`,`info`,`status`) VALUES (%s,%s,%s,%s)".format ()
                    sql_save = ('Ответ',lastid,message_text,'')
                    cursor.execute(sql,sql_save)
                    db.commit()       
                    time.sleep (5)
                else:
                    sql = "UPDATE task SET info = '{}' WHERE data_id = {} and name = 'Статус' ".format ('Пропуск',lastid)
                    cursor.execute(sql)
                    db.commit() 
            else:
                print ('            [+] Пропуск новостей т.к. уже былы')
            #exit(0)  
    time.sleep (600)
    
    
    
if options.menu == '25': 
    print ('Собирает информацию в телеграмм')
    setting = {'namebot':'nnmclub314_bot'}    
    set_print ('Собирает информацию в телеграмм',setting,'Main')   
    
    
    
    
    
    connect_info = {'host':'localhost','user':'izofen','password':'podkjf4','database':'telegram'} 
    db,cursor = connect (connect_info)  
    sql = "select id,catalog_id,vk_name,vk_id,phone_number,depth from catalog_name where id = {} ".format ( options.city)
    cursor.execute(sql)
    data = cursor.fetchall()
    id = 0
    for rec in data: 
        id,catalog_id,vk_name,vk_id,phone_number,depth = rec.values()            
        print (id,catalog_id,vk_name,vk_id,phone_number,depth)    
    #set_start ('Днем',5,24)     
    import iz_bot  
    import time  
    #phone_number = 634
    api_id   = int(setting.setdefault('api_id',192804))      #192804
    api_hash = str(setting.setdefault('api_hash','1b40d1d01f8922b384d44e29d32f6acf'))   #'1b40d1d01f8922b384d44e29d32f6acf'    
    client,answer = telegram_connect (phone_number,api_id,api_hash)   
    print ('[+] answer:',answer)      
    #depth       = 1000
    name_dialog = int(catalog_id)
    messages =  get_message (client,name_dialog,depth)
    for message in messages:
        message_id      = message.id        
        message_text    = message.text        
        print ('        [+] Новость: ',message_id)
        message_text    = str(message_text).strip()   
        connect_info = {'host':'localhost','user':'izofen','password':'podkjf4','database':'telegram'} 
        db,cursor = connect (connect_info)  
        unixtime = int (time.time ())        
        sql = "select id,catalog_in from message_save where message_id = {} and catalog_in = '{}' ".format (message_id,catalog_id)
        cursor.execute(sql)
        data = cursor.fetchall()
        id = 0
        for rec in data: 
            id,catalog_in = rec.values()            
        if id == 0:
            filename = 'C:/Apache24/Telegram/'+str(vk_id)+'/pict_'+str(name_dialog)+' '+str(message_id)
            filename = client.download_media(message, filename)
            print (filename)
            sql = "INSERT INTO message_save (`accound`,`catalog_in`,`message`,`message_id`,`text`,`unixtime`,`picture`) VALUES (%s,%s,%s,%s,%s,%s,%s)".format ()
            sql_save = ('+79033671563',str(name_dialog),str(message),message_id,message_text,unixtime,str(filename))
            cursor.execute(sql,sql_save)
            db.commit() 
            time.sleep (10)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
if options.menu == '24': 
    print ('Читаем каталог отправляем в бота')
    setting = {'namebot':'junctionA123_bot'}    
    set_print ('Читаем каталог отправляем в бота',setting,'Main')   
    set_start ('Днем',5,24)     
    import iz_bot  
    import time    
    host = '127.0.0.1'       
    user = 'izofen'
    password = 'podkjf4'
    database = 'junctionA123_bot'
    connect_info = {'host':host,'user':user,'password':password,'database':database} 
    #setting = iz_bot.get_setting ({'namebot':'@law_help_bot'})  
    api_id   = int(setting.setdefault('api_id',192804))      #192804
    api_hash = str(setting.setdefault('api_hash','1b40d1d01f8922b384d44e29d32f6acf'))   #'1b40d1d01f8922b384d44e29d32f6acf'
    db,cursor = connect (connect_info)  
    #sql = "select id,info from service where name = 'Слово'"
    #cursor.execute(sql)
    #data = cursor.fetchall()
    #list = []
    #for rec in data: 
    #    id,info = rec.values()
    #    list.append (info)
    phone_number = 634
    client,answer = telegram_connect (phone_number,api_id,api_hash)
    print ('[+] answer:',answer)
    sql = "select id,info from service where name = 'Группа'"
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data: 
        id,info = rec.values()       
        name_dialog = info
        print ('    [+] Группа: ',name_dialog)
        depth       = 10
        messages =  get_message (client,name_dialog,depth)
        time.sleep (10)
        for message in messages:
            message_id      = message.id        
            message_text    = message.text
            print ('        [+] Новость: ',message_id)
            message_text    = str(message_text).strip()            
            sql = "select t1.id,t1.name from task as t1, task as t2 where t1.data_id = t2.data_id and t1.name = 'Задание' and t1.info = '"+str(message.id)+"' and t2.name = 'Группа' and t2.info = '"+str(name_dialog)+"'"
            print ('[sql]',sql)
            cursor.execute(sql)
            data = cursor.fetchall()
            id = 0
            for rec in data: 
                id,name = rec.values() 
            if id == 0:                      
                print ('[+] Записываем ...')
                sql = "INSERT INTO task (`name`,`data_id`,`info`,`status`) VALUES ('Задание',0,'{}','')".format (str(message_id))
                cursor.execute(sql)
                db.commit()  
                lastid = cursor.lastrowid
                sql = "UPDATE task SET data_id = {} WHERE id = {} ".format (lastid,lastid)
                cursor.execute(sql)
                db.commit() 
                sql = "INSERT INTO task (`name`,`data_id`,`info`,`status`) VALUES ('Группа',{},'{}','')".format (lastid,name_dialog)
                cursor.execute(sql)
                db.commit()  
                sql = "INSERT INTO task (`name`,`data_id`,`info`,`status`) VALUES ('Статус',{},'{}','')".format (lastid,"Записан")
                cursor.execute(sql)
                db.commit()  
                sql = "INSERT INTO task (`name`,`data_id`,`info`,`status`) VALUES (%s,%s,%s,%s)".format ()
                sql_save = ('Текст',lastid,message_text,'')
                cursor.execute(sql,sql_save)
                db.commit()          
        
        
                word_search = ""
        #        for line in list:
        #            print ('             [+] Поиск слова:',line)
        #            if message_text.find (line) != -1:
        #                word_search = word_search + ", " + str(line)
                #if word_search != '':
                if 1==1:
                
                    message_info = {"user_id":"399838806","namebot":database}
                    
                    message_text = message_text.replace ('\\','')
                    message_text = message_text.replace ('**','')
                    
                    send_data = {"Text":message_text,'Запись в базу':'Не записывать'}
                    
                    
                    try:
                        iz_bot.send_message (message_info,send_data)  
                    except Exception as e:
                        print ('[+] message_text',message_text)
                        time.sleep (600)
                
                
        #            answer  = send_forward_catalog (client,'-1001846436203',message) 
        #            answer  = send_message_catalog (client,'-1001846436203',str(word_search))   
        #            time.sleep (60)
        #            sql = "UPDATE task SET status = '{}' WHERE id = {} ".format ('Отправлен',lastid)
        #            cursor.execute(sql)
        #            db.commit()
        #            sql = "INSERT INTO task (`name`,`data_id`,`info`,`status`) VALUES (%s,%s,%s,%s)".format ()
        #            sql_save = ('Ответ',lastid,message_text,'')
        #            cursor.execute(sql,sql_save)
        #            db.commit()       
        #            time.sleep (5)
        #        else:
        #            sql = "UPDATE task SET info = '{}' WHERE data_id = {} and name = 'Статус' ".format ('Пропуск',lastid)
        #            cursor.execute(sql)
        #            db.commit() 
            else:
                print ('            [+] Пропуск новостей т.к. уже былы')
            #exit(0)  
    #time.sleep (600)    
