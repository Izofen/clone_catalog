#!/usr/bin/python
# -*- coding: utf-8


def connect (namebot):
    import pymysql 
    base = namebot.replace("@","")
    db = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database=base,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)        
    cursor = db.cursor()
    return db,cursor
        
def change (word):
    word = word.replace("'","<1>")
    word = word.replace('"',"<2>")
    word = word.replace('/',"<3>")
    word = word.replace(')',"<4>")
    word = word.replace('(',"<5>")
    return (word)

def change_back (word):
    word = word.replace("#1#","'")
    word = word.replace("#2#",'"')
    word = word.replace("#3#",'/')
    word = word.replace("#4#",')')
    word = word.replace("#5#",'(')
    word = word.replace("#",'"')
    return (word)

def build_jsom (dict):    #### {"o":"next","sql":id_sql}
    json_message = str(dict)
    json_message = json_message.replace ("'",'"')
    json_message = json_message.replace ('"','#')
    #json_message = change(json_message)
    json_message = "i_"+json_message
    json_message = json_message.replace (", ",',')
    json_message = json_message.replace (": ",':')
    return (json_message)

def user_get_data (message_info,get_data):
    namebot = message_info['namebot']
    user_id = message_info['user_id']
    db,cursor = connect (namebot)
    connect (namebot)
    data_answer = {}
    sql = "select id,name,info,data_id from users where name = 'user_id' and info = '{}' ;".format (user_id)
    cursor.execute(sql)
    results = cursor.fetchall()    
    for row in results:
        id,name,info,data_id = row.values() 
        #data_answer[name] = info
        sql = "select id,name,info from users where data_id = '{}' ;".format (data_id)
        cursor.execute(sql)
        results = cursor.fetchall()    
        for row in results:
            id,name,info = row.values() 
            #print (id,name,info)
            data_answer[name] = info
    return data_answer 

def save_FIO (message_info):
    import time
    namebot    = message_info ['namebot']
    first_name    = message_info ['first_name']
    last_name    = message_info ['last_name']
    username    = message_info ['username']
    db,cursor = connect (namebot)
    user_id = message_info ['user_id'] 
    sql = "select id,name from users where name = 'user_id' and info = '"+str(user_id)+"' limit 1" 
    cursor.execute(sql)
    results = cursor.fetchall()        
    id = 0
    for row in results:    
        id,name = row.values()
    #    sql = "UPDATE bot_user SET timestamp = "+str(time.time())+" WHERE id = "+str(id)+""
    #    cursor.execute(sql)
    #    db.commit()
    #    sql = "UPDATE bot_user SET send_message = '' WHERE id = "+str(id) + ""
    #    cursor.execute(sql)
    #    db.commit()  
    if id == 0:
    #    timestamp = int(time.time())
    #    cursor = db.cursor() 
        sql = "INSERT INTO users (`name`,`info`,`data_id`,`status`) VALUES ('{}','{}',{},'')".format ('user_id',str(user_id),0)
        cursor.execute(sql)
        db.commit()  
        lastid = cursor.lastrowid
        
        sql = "UPDATE users SET data_id = {} WHERE id = {}".format(lastid,lastid)
        cursor.execute(sql)
        db.commit()
        
        sql = "INSERT INTO users (`name`,`info`,`data_id`,`status`) VALUES ('{}','{}',{},'')".format ('first_name',str(first_name),lastid)
        cursor.execute(sql)
        db.commit()  
        
        sql = "INSERT INTO users (`name`,`info`,`data_id`,`status`) VALUES ('{}','{}',{},'')".format ('last_name',str(last_name),lastid)
        cursor.execute(sql)
        db.commit()  
        
        sql = "INSERT INTO users (`name`,`info`,`data_id`,`status`) VALUES ('{}','{}',{},'')".format ('username',str(username),lastid)
        cursor.execute(sql)
        db.commit()  
        
        sql = "INSERT INTO users (`name`,`info`,`data_id`,`status`) VALUES ('{}','{}',{},'')".format ('time_start',str(int(time.time())),lastid)
        cursor.execute(sql)
        db.commit()
        

        
        
    #    lastid = cursor.lastrowid
    #    id = 0
    db.close    
        
def dict (menu,name,empty):
    try:
        text = menu[name]
    except:    
        text = empty
    return text

def get_menu  (message_info,menu_data): 

    import json
    markup = ''
    namebot    = message_info ['namebot']
    #name       = menu_data    ['Имя меню']
    name       = menu_data.setdefault ('Имя меню','')
    key_array  = menu_data    ['Кнопки']
    db,cursor = connect (namebot)
    connect (namebot)
    data_menu = {}
    data_menu ['Тип кнопки'] = menu_data.setdefault('Тип кнопки','Клавиатура')

    if key_array != '':
        number = 0
        for line in key_array: 
            number = number + 1
            data_menu ['Кнопка ' +str(number)+'1'] = line[0][0]
            data_menu ['Кнопка ' +str(number)+'2'] = line[1][0]
            data_menu ['Кнопка ' +str(number)+'3'] = line[2][0]
            data_menu ['Команда '+str(number)+'1'] = line[0][1]
            data_menu ['Команда '+str(number)+'2'] = line[1][1]
            data_menu ['Команда '+str(number)+'3'] = line[2][1]

    if name != '':    
        sql = "select id,name,info from menu where name = 'Имя' and info = '{}' ;".format (name)
        cursor.execute(sql)
        results = cursor.fetchall()    
        for row in results:
            id,name,info = row.values() 
            data_menu[name] = info
        sql = "select id,name,info from menu where  data_id = '{}' ;".format (id)
        cursor.execute(sql)
        results = cursor.fetchall()    
        for row in results:
            id,name,info = row.values() 
            data_menu[name] = info
            
            
    if data_menu['Тип кнопки'] == 'Сообщение':    
        line = []
        for number in range(30):
            line1  = []
            key11  = {}
            key11['text']          = data_menu.setdefault('Кнопка ' +str(number+1)+'1','')
            key11['callback_data'] = data_menu.setdefault('Команда '+str(number+1)+'1','')
            key12  = {}
            key12['text']          = data_menu.setdefault('Кнопка ' +str(number+1)+'2','')
            key12['callback_data'] = data_menu.setdefault('Команда '+str(number+1)+'2','')
            key13  = {}
            key13['text']          = data_menu.setdefault('Кнопка ' +str(number+1)+'3','')
            key13['callback_data'] = data_menu.setdefault('Команда '+str(number+1)+'3','')
            if data_menu.setdefault('Кнопка ' +str(number+1)+'1','') != '':        
                line1.append(key11)
            if data_menu.setdefault('Кнопка ' +str(number+1)+'2','') != '':
                line1.append(key12)
            if data_menu.setdefault('Кнопка ' +str(number+1)+'3','') != '':        
                line1.append(key13)
            line.append(line1)    
        array = {"inline_keyboard":line}               

    if data_menu['Тип кнопки'] == 'Клавиатура':    
        array  = {}        
        line   = []
        for number in range(3):
            line1  = []
            key11  = {}
            key11['text'] = data_menu.setdefault('Кнопка '+str(number)+'1','')        
            if data_menu.setdefault('Замена '+str(number)+'1','') != '':
                key11['text'] = data_menu.setdefault('Замена '+str(number)+'1','')        
            line1.append(key11)
            key12 = {}
            key12['text'] = data_menu.setdefault('Кнопка '+str(number)+'2','')
            if data_menu.setdefault('Замена '+str(number)+'2','') != '':
                key12['text'] = data_menu.setdefault('Замена '+str(number)+'2','')
            line1.append(key12)    
            key13 = {}
            key13['text'] = data_menu.setdefault('Кнопка '+str(number)+'3','')
            if data_menu.setdefault('Замена '+str(number)+'3','') != '':
                key13['text'] = data_menu.setdefault('Замена '+str(number)+'3','')
            line1.append(key13)        
            line.append(line1)
        array = {"keyboard":line,"resize_keyboard":True}  

    markup = json.dumps(array)      
    return markup

def get_setting (message_info):
    namebot = message_info['namebot']
    db,cursor = connect (namebot)
    data_answer = {}
    sql = "select id,name,info from setting where 1=1".format ()
    cursor.execute(sql)
    results = cursor.fetchall()    
    for row in results:
        id,name,info = row.values() 
        data_answer[name] = info
    return data_answer 
      
def get_message (message_info,info_data):
    namebot = message_info.setdefault ('namebot')
    name    = info_data.setdefault ('Имя','')
    db,cursor = connect (namebot) 
    data_message = {}
    sql = "select id,name,info from message where name = 'Имя' and info = '{}' ;".format (name)
    print ('[sql]',sql)
    cursor.execute(sql)
    results = cursor.fetchall()    
    id = 0
    for row in results:
        id,name,info = row.values() 
        if id != 0:
            sql = "select id,name,info from message where data_id = {};".format (id)
            cursor.execute(sql)
            results = cursor.fetchall()    
            for row in results:
                id,name,info = row.values() 
                data_message[name] = info
    return data_message    

def send_message (message_info,send_data):
    import requests
    answer  = 'Ответ'
    setting = get_setting (message_info)
    token    = setting.setdefault ('Токен','')
    menu_name    = ''
    message_out  = ''
    picture      = ''
    menu_list    = ''
    message_type = ''
    data_message = {}
    namebot    = message_info.setdefault ('namebot','')
    message_in = message_info.setdefault ('message_in','')
    message_id = message_info.setdefault ('message_id','')    
    avtomat    = message_info.setdefault ('Автомат','')   
    db,cursor = connect (namebot)    
    key_array  = send_data.setdefault ('Кнопки','')
    only_text  = send_data.setdefault ('Text','')
    type_text  = send_data.setdefault ('Тип','Из базы')
    method     = send_data.setdefault ('Метод','sendMessage')
    save_base  = send_data.setdefault ('Запись в базу','Записать')
    type_key   = send_data.setdefault ('Тип кнопки','Клавиатура')
    name_picture = send_data.setdefault ('Картинка','')      
    user_id = send_data.setdefault('user_id','')
    if user_id == '':
        user_id = message_info.setdefault('user_id','') 
    message = message_in

    ############################################################################## ПОЛУЧЕНИЕ ПЕРВОГО ТЕСТА #####################################################################
    if only_text != '':
        data_message['Текст'] = only_text
        id = 0
        sql = "select id,name from message where name = 'Имя' and info = '{}' ;".format(only_text)
        cursor.execute(sql)
        data = cursor.fetchall()
        for rec in data:
            id,name = rec.values()     
        if id == 0:    
            if save_base != 'Не записывать':
                sql = "INSERT INTO message (data_id,info,name,status) VALUES ({},'{}','{}','')".format (0,only_text,'Имя')
                cursor.execute(sql)
                db.commit()
                lastid = cursor.lastrowid
                sql = "INSERT INTO message (data_id,info,name,status) VALUES ({},'{}','{}','')".format (lastid,only_text,'Текст')
                cursor.execute(sql)
                db.commit()
        message  = only_text     
        message_out = only_text
        
    ############################################################################ Поиск сообщения в базе ########################################################################################################################
        
    print ('[message_in]',message_in)    
    message_in  = message_in.replace('\\','')    
    sql = 'select id,name,info from message where name = "Имя" and info = "{}" ;'.format (message)
    cursor.execute(sql)
    results = cursor.fetchall()    
    id = 0
    for row in results:
        id,name,info = row.values() 
        if id != 0:
            sql = "select id,name,info from message where data_id = {};".format (id)
            cursor.execute(sql)
            results = cursor.fetchall()    
            for row in results:
                id,name,info = row.values() 
                data_message[name] = info
                
    ##################################################### [Делаем замену сообщений] ##################################################################################################
                
    message_out = data_message.setdefault('Текст'  ,'')             

    if send_data.setdefault('Замена','')  != '':
        for line in send_data.setdefault('Замена',''):
            print ('[line]',line)
            message_out = message_out.replace(str(line[0]),str(line[1]))                                
    if send_data.setdefault('Автомат','') == 'Да' and  data_message.setdefault('Автомат','' == 'Нет'):
        message_out = ''
    else:   
        pass
        
    menu_name = data_message.setdefault('Меню'  ,'')     
    if menu_name != '' or key_array != '':
        menu_data = {'Имя меню':menu_name,'Кнопки':key_array,'Тип кнопки':type_key}
        markup = get_menu  (message_info,menu_data) 


    if message_out != '':
        if method == "sendMessage":
            params = {}
            params['chat_id'] = user_id   ##"399838806"                
            params['text'] = message_out
            params['parse_mode'] = 'HTML'
            if menu_name != '' or key_array != '':
                params['reply_markup'] = markup
            url  = 'https://api.telegram.org/bot{0}/{1}'.format(token, method)
            resp = requests.post(url, params) 
            answer = resp.json()
            print ('[+]👧------------------------------------------------------------ [Ответ Отправки] -------------------------------------------------------👧[+]') 
            print ( answer)
            print ('[+]👧------------------------------------------------------------ [Ответ Отправки] -------------------------------------------------------👧[+]') 
            print ('')
            
        if method == "editMessageText":
            params = {}
            params['chat_id']    = user_id
            params['text']       = str(message_out)
            params['message_id'] = message_id
            params['parse_mode'] = 'HTML'
            if menu_name != '' or key_array != '':
                params['reply_markup'] = markup
            url  = 'https://api.telegram.org/bot{0}/{1}'.format(token, method)
            resp = requests.post(url, params) 
            answer = resp.json()
            print (    '[Ответ Отправки] :',answer)


        if method == "sendPhoto":
            params = {}
            params['chat_id'] = user_id
            params['caption'] = str(message_out)
            params['parse_mode'] = 'HTML'
            if menu_name != '' or key_array != '':
                params['reply_markup'] = markup
            file_path = name_picture
            print ('[+] name_picture',name_picture)
            file_opened = open(file_path, 'rb')
            files = {'photo': file_opened}
            url='https://api.telegram.org/bot{0}/{1}'.format(token, method)            
            resp = requests.post(url, params, files=files)
            answer = resp.json()   
            print (    '[Ответ Отправки] :',answer)    

        if method == "editMessageCaption":
            params = {}
            params['chat_id'] = user_id
            params['caption'] = str(message_out)
            params['message_id'] = message_id
            params['parse_mode'] = 'HTML'
            if menu_name != '' or key_array != '':
                params['reply_markup'] = markup
            file_path = name_picture
            print ('[+] name_picture',name_picture)
            file_opened = open(file_path, 'rb')
            files = {'photo': file_opened}
            url='https://api.telegram.org/bot{0}/{1}'.format(token, method)            
            resp = requests.post(url, params, files=files)
            answer = resp.json()   
            print (    '[Ответ Отправки] :',answer)      


        if method == "editMessageMedia":
            import json
            file_path = name_picture 
            files = {'media': open(file_path, 'rb'),}
            media = json.dumps({'type': 'photo','media': 'attach://media'})
            method = 'editMessageMedia'
            #markup = json.dumps(array)
            url    = 'https://api.telegram.org/bot{0}/{1}'.format(token, method)   #?chat_id=399838806&message_id=871&media='+str(media)+''
            params = {'chat_id': user_id,'message_id':message_id,'media':media,'reply_markup':markup,'caption':'444444444444444444'}
            resp = requests.post(url, params,files = files)                
            print (resp.json())
    return answer

def sendDice (user_id,namebot):
    import requests
    import iz_telegram
    import json
    setting = get_setting (message_info)
    token    = setting.setdefault ('Токен','')
    method = "sendDice"
    params = {'chat_id': user_id} 
    url='https://api.telegram.org/bot{0}/{1}'.format(token, method)
    resp = requests.post(url, params)
    answer = resp.json()
    print ('[sendDice]',answer)
    return resp.json()

def user_save_data (message_info,save_data): 
    #### ИСПРАВИТЬ ID И DATA_ID   
    namebot = message_info['namebot']
    user_id = message_info['user_id']
    print ('    [+] Запись информации в базу данных:',user_id)
    db,cursor = connect (namebot)
    connect (namebot)
    data_answer = {}
    data_id     = 0
    sql = "select id,name,info,data_id from users where name = 'user_id' and info = '{}' ;".format (user_id)
    print ('[sql]',sql)
    cursor.execute(sql)
    results = cursor.fetchall()    
    for row in results:
        id_save,name,info,data_id = row.values() 
        sql = "select id,name,info from users where data_id = {} ;".format (id_save)
        cursor.execute(sql)
        results = cursor.fetchall()  
        for row in results:
            id,name,info = row.values() 
            data_answer[name] = info
        for line in save_data:
            if data_answer.setdefault(line[0],'not in base') == 'not in base':
                print ('    [+] Праметр:',line,' - Записать новый')
                sql = "INSERT INTO users (data_id,info,name,status) VALUES ({},'{}','{}','')".format (id_save,str(line[1]),str(line[0]))
                cursor.execute(sql)
                db.commit() 
            else:       
                print ('    [+] Праметр:',line,' - Обновить')
                sql = "UPDATE users SET info = '"+str(line[1])+"' WHERE `name` = '"+str(line[0])+"' and data_id = "+str(id_save)+" "
                cursor.execute(sql)
                db.commit()
                
def deleteMessage (message_info,message_id):
    import requests
    namebot = message_info['namebot']
    setting = get_setting (message_info)
    token    = setting.setdefault ('Токен','')
    user_id = message_info['user_id']
    method = "deleteMessage"
    params = {'chat_id': user_id,'message_id':message_id} 
    url='https://api.telegram.org/bot{0}/{1}'.format(token, method)
    resp = requests.post(url, params)
    answer = resp.json()
    print ('[deleteMessage]',answer)
    return resp.json()    

def task_save_data (message_info,save_data):
    namebot     = message_info['namebot']
    id_task     = save_data['id_task']
    name_task   = save_data['Параметр'] 
    db,cursor = connect (namebot)
    connect (namebot)
    data_answer = {}
    data_id     = 0
    sql = "select id,name,info,data_id from task where id = {};".format (id_task)
    cursor.execute(sql)
    results = cursor.fetchall()    
    for row in results:
        id,name,info,data_id = row.values() 
        sql = "select id,name,info from task where data_id = '{}' ;".format (data_id)
        cursor.execute(sql)
        results = cursor.fetchall()    
        for row in results:
            id,name,info = row.values() 
            data_answer[name] = info

        for line in name_task:
            print (line)
            if data_answer.setdefault(line[0],'not in base') == 'not in base':
                sql = "INSERT INTO task (data_id,info,name,status) VALUES ({},'{}','{}','')".format (data_id,str(line[1]),str(line[0]))
                cursor.execute(sql)
                db.commit() 
            else:       
                sql = "UPDATE task SET info = '"+str(line[1])+"' WHERE `name` = '"+str(line[0])+"' "
                cursor.execute(sql)
                db.commit()    

def task_get_data (message_info,get_data):
    namebot = message_info['namebot']
    id_task     = get_data['id_task']
    db,cursor = connect (namebot)
    connect (namebot)
    data_answer = {}
    sql = "select id,name,info from task where data_id = '{}' ;".format (id_task)
    cursor.execute(sql)
    results = cursor.fetchall()    
    for row in results:
        id,name,info = row.values() 
        data_answer[name] = info
    return data_answer                 
