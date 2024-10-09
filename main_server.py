#!/usr/bin/python
# -*- coding: utf-8

from flask import Flask
from flask import request
app = Flask(__name__)

from threading import Thread

def connect (namebot): 
    import pymysql
    db = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database = namebot,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()  
    return db,cursor
       
def update_key (name_key1,name_key2,key11,data_id,namebot):
    db,cursor = connect (namebot)     
    id = 0
    sql = "select id,data_id from menu  where name = '{}' and data_id = {} limit 1;".format (name_key1,data_id)
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data: 
        id,name  =  rec.values()    
    if id == 0:
        sql = "INSERT INTO `menu` (`name`,`data_id`,`info`,`status`) VALUES ('{}',{},'{}','{}')".format (name_key1,data_id,key11,'')
        sql_save = ()
        cursor.execute(sql,sql_save)
        lastid = cursor.lastrowid 
        db.commit()            
    else:    
        sql = "UPDATE menu SET `info` = '{}' WHERE name = '{}' and data_id = {} ".format (key11,name_key1,data_id)
        sql_save = ()
        cursor.execute(sql,sql_save)  
        db.commit()      
    id = 0
    sql = "select id,data_id from menu  where name = '{}' and data_id = {} limit 1;".format (name_key2,data_id)
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data: 
        id,name  =  rec.values()    
    if id == 0:
        sql = "INSERT INTO `menu` (`name`,`data_id`,`info`,`status`) VALUES ('{}',{},'{}','{}')".format (name_key2,data_id,key11,'')
        sql_save = ()
        cursor.execute(sql,sql_save)
        lastid = cursor.lastrowid 
        db.commit()            
    else:    
        sql = "UPDATE menu SET `info` = '{}' WHERE name = '{}' and data_id = {} ".format (key11,name_key2,data_id)
        sql_save = ()
        cursor.execute(sql,sql_save)  
        db.commit()      

class start_bot (Thread):
    def __init__(self,message_info):
        Thread.__init__(self)
        self.message_info            = message_info
        
    def run(self):
        message_info                 = self.message_info
        namebot    = message_info.setdefault('namebot','')
        namebot    = namebot.replace("@","")
        mycode = 'import start_{}'.format (namebot)
        exec(mycode)        
        mycode = 'start_{}.start_prog (message_info)'.format(namebot)
        exec(mycode)
                     
@app.route('/telegram/<access_code>/<namebot>/', methods=["GET", "POST"])   ### <access_code>/<namebot>/
def telegram (access_code,namebot):     ### 
    import iz_general
    import iz_bot
    print ('[+] namebot:',namebot)
    if namebot == '@VK314_bot':
        return {"ok": False}
    if request.method == "POST":
        parsed_string = request.json        
        message_info = iz_general.parsed_string (parsed_string)  
        if message_info.setdefault('sender_chat_username','')  != '':  
            import requests
            import json
            user_id = -1001644105615
            message_out = 'Проверка работы системы'
            token       = '6422168947:AAGy4pzndN1WYgMyFRf_mVXF6gEptDpzLz0'
            method      = "editMessageText"
            import iz_bot
            db,cursor = iz_bot.connect ('bot_main') 
            sql = "select id,key01,key02,key03,key_press01,key_press02,key_press03 from key_message where name = 'Тестовая кнопка' limit 1"
            cursor.execute(sql)
            results = cursor.fetchall()        
            for row in results: 
                id,key01,key02,key03,key_press01,key_press02,key_press03 = row.values()            
            if str(message_info['callback'].find ('i_')) != -1:
                import json
                import requests
                json_string  = iz_bot.change_back(message_info['callback'].replace('i_',''))
                data_json = json.loads(json_string)
                operation = data_json.setdefault('o','')
                nomer     = data_json.setdefault('p','')  
                key_pres  = data_json.setdefault('k','') 
                print ('    [+] operation:',operation)    
                print ('    [+] nomer    :',nomer)    
            if operation == 'grup':
                if key_pres == 1:
                    sql = "UPDATE key_message SET key_press01 = key_press01 + 1 WHERE name = 'Тестовая кнопка' ".format ()
                    sql_save = ()
                    cursor.execute(sql,sql_save)
                    db.commit()
                if key_pres == 2:
                    sql = "UPDATE key_message SET key_press02 = key_press02 + 1 WHERE name = 'Тестовая кнопка' ".format ()
                    sql_save = ()
                    cursor.execute(sql,sql_save)
                    db.commit()
            sql = "select id,key01,key02,key03,key_press01,key_press02,key_press03 from key_message where name = 'Тестовая кнопка' limit 1"
            cursor.execute(sql)
            results = cursor.fetchall()        
            for row in results: 
                id,key01,key02,key03,key_press01,key_press02,key_press03 = row.values()
                line = []
                line1  = []
                key11  = {}
                key11['text']          =  str(key01) + ' ' + str(key_press01)
                key11['callback_data'] =  iz_bot.build_jsom({"o":'grup',"p":id,"k":1})
                key12  = {}
                key12['text']          =  str(key02) + ' ' + str(key_press02)
                key12['callback_data'] =  iz_bot.build_jsom({"o":'grup',"p":id,"k":2})
                key13  = {}
                line1.append(key11)
                line1.append(key12)
                #line1.append(key13)
                line.append(line1)    
                array = {"inline_keyboard":line}  
                markup = json.dumps(array)            
                params = {}
                params['chat_id'] = user_id                  
                params['text'] = message_out
                params['parse_mode'] = 'HTML'
                params['message_id'] = message_info['message_id']
                #if menu_name != '' or key_array != '':
                params['reply_markup'] = markup      
                #    print ('[markup]:',markup)                
                url  = 'https://api.telegram.org/bot{0}/{1}'.format(token, method)
                resp = requests.post(url, params) 
                answer = resp.json()
                print ('[+]👧------------------------------------------------------------ [Ответ Отправки] -------------------------------------------------------👧[+]') 
                print ( answer)
                print ('[+]👧------------------------------------------------------------ [Ответ Отправки] -------------------------------------------------------👧[+]') 
                print ('')        
        db,cursor   = iz_bot.connect (namebot)         
        message_in   = message_info.setdefault('message_in')
        message_new  = message_info.setdefault('message_in',message_in)        
        message_in   = message_in.replace('\\','')
        sql = 'select id,name,info,data_id from menu where name like %s and info = %s ;'.format ()
        sql_save = ('Замена%',message_in)
        cursor.execute(sql,sql_save)
        results = cursor.fetchall()    
        for row in results:
            id,name,info,data_id = row.values()
            name_new = name.replace("Замена ","")
            sql = "select id,name,info from menu where  data_id = {} and name = 'Кнопка {}';".format (data_id,name_new)
            cursor.execute(sql)
            results = cursor.fetchall()    
            for row in results:
                id,name,info = row.values() 
            message_new = info
        message_info['message_in']   = message_new 
        message_info['message_old']  = message_in 
        message_info['namebot']      = namebot 
        print ('[+]🌹--------------------------------------------------------------- [message_info] -------------------------------------------------------🌹[+]')
        print (message_info)
        print ('[+]🌹--------------------------------------------------------------- [message_info] -------------------------------------------------------🌹[+]')
        print ('')
        FIO_id = iz_bot.save_FIO (message_info)
        send_data = {'Автомат':'Да'}
        iz_bot.send_message (message_info,send_data) 
        my_thread = start_bot (message_info)
        my_thread.start()
    print ('[+] --------------------------------------------------- [Запуск отдельного потока] ---------------------------------------------------------')    
    print ('')   
    return {"ok": True}

@app.route('/vk_crisp/', methods=["GET", "POST"])   ### 
def vk_crisp ():   ### 
    print ('[vk_crisp]:',vk_crisp)
    namebot = "TEST"
    user_id = "TEST"
    message = "TEST"
    #import iz_func
    #import iz_vk
    from flask import request
    if request.method == "POST":
        print ('[+]----vk_crisp 1.100--------------------------------------------------------------[+]')
        print (request.json)
        print ('[+]--------------------------------------------------------------------------[+]')        
        parsed_string   = request.json
        website_id_main   = parsed_string.setdefault('website_id','')
        event_main        = parsed_string.setdefault('event','')
        if event_main == 'message:send':
             return 'ok'
        data_main         = parsed_string.setdefault('data','')    
        website_id        = data_main.setdefault('website_id','')
        type_t            = data_main.setdefault('type','')
        from_t            = data_main.setdefault('from','')
        origin            = data_main.setdefault('origin','')
        content           = data_main.setdefault('content','')
        fingerprint       = data_main.setdefault('fingerprint','')
        user              = data_main.setdefault('user','')
        nickname_user     = ''
        nickname_user_id  = ''
        if user != '':
            nickname_user     = user.setdefault('nickname','')
            nickname_user_id  = user.setdefault('user_id','')        
        mentions          = data_main.setdefault('mentions','')
        timestamp         = data_main.setdefault('timestamp','')
        stamped           = data_main.setdefault('stamped','')
        session_id        = data_main.setdefault('session_id','')
        print ('[+] website_id_main:',website_id_main)
        print ('[+] event_main:',event_main)
        print ('[+] data_main',data_main)
        print ('[+] data_main',type(data_main))
        print ('[+] user:',user)
        print ('[+] nickname_user:',nickname_user)
        print ('[+] nickname_user_id:',nickname_user_id)
        print ('[+] session_id:',session_id)
        print ('[+] content:',content)
        message_out = content;
        base = "crisp"
        import pymysql
        db = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database=base,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)  
        cursor = db.cursor()   
        sql = "select id,name,user_id,mesage_in from session where session_id = '{}'  limit 1;".format (session_id)  #### and status <> 'resolved'       
        cursor.execute(sql)
        results = cursor.fetchall()    
        user_id_i = 0
        id_i = 0
        for row in results:
            id_i,name_i,user_id_i,mesage_in_i = row.values() 
            print ('[+] id_i',id_i,name_i,user_id_i,mesage_in_i)
        user_id = user_id_i
        if str(message_out).find ('state:resolved') != -1:
            sql = "UPDATE session SET status = '{}' WHERE id  = '{}'".format ('resolved',id_i)
            cursor.execute(sql)
            db.commit()
        if message_out != '' and user_id != 0 and str(message_out).find ('state:resolved') == -1 :
            print ('    [+] message_out:',message_out)    
            print ('    [+] user_id:',user_id)    
            import vk_api
            from vk_api.keyboard import VkKeyboard, VkKeyboardColor
            from vk_api.utils import get_random_id  
            apikey_avtor = 'vk1.a.2mtlxCdi94HCl_o58vujcLqJEqn4bRamn8LJ4h-eJaVqtllvkfIg8ngj0AJX6OMrNVBn0w0ggFNGAB--JmPz0oYJ4hf4n48P91oM2KOb86st1cPE7jqOqE5HW0sO5d0JJtlhXlmG0oTHG3xRqJvj06oXqqf006nluEfj3pu3NrGSA1boxVtHUoNX8d-ytjPvrIWRUKspSrvBn5aiyreQnw'
            vk_session = vk_api.VkApi(token=apikey_avtor)
            vk = vk_session.get_api() 
            vk.messages.send(peer_id=user_id,random_id=get_random_id(),message=message_out)
            sql = "UPDATE session SET message_out = '{}' WHERE id  = '{}'".format (message_out,id_i)
            cursor.execute(sql)
            db.commit()
    return 'ok'

@app.route('/vkmessage/', methods=["GET", "POST"])   ### 
def vkmessage ():   ### 
    namebot = "TEST"
    user_id = "TEST"
    message = "TEST"
    import iz_vk
    from flask import request
    if request.method == "POST":
        print ('[+]----VK 1. 224--------------------------------------------------------------[+]')
        print (request.json)
        print ('[+]--------------------------------------------------------------------------[+]')        
        parsed_string   = request.json
        type_message = parsed_string['type']
        group_id     = parsed_string['group_id']
        event_id = parsed_string.setdefault('event_id','')  
        try:
            message  = parsed_string['object']['message']['text']        
        except:    
            message  = ''
        try:
            user_id  = parsed_string['object']['message']['peer_id']        
        except:    
            user_id  = ''
        print ('[+] user_id:',user_id)
        print ('[+] message:',message)
        print ('[+] event_id:',event_id)
        print ('[+] group_id:',group_id)
        print ('[+] type_message:',type_message)
        import pymysql 
        connect_info = {'host':'127.0.0.1','user':'izofen','password':'podkjf4','database':'vk_'+str(group_id)}
        print ('[+] connect_info:',connect_info)
        try:
            db = pymysql.connect(host=connect_info['host'],user=connect_info['user'],password=connect_info['password'],database=connect_info['database'],charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)  
            cursor = db.cursor() 
        except:
            return 'error'
        sql = "select id from event where name = '{}' limit 1".format (event_id)
        cursor.execute(sql)
        results = cursor.fetchall()    
        id = 0
        for row in results:
            id = row['id']
        if id == 0:
            sql = "INSERT INTO event (`name`) VALUES ('{}')".format (event_id)
            cursor.execute(sql)
            db.commit()
        event_id = id
        if type_message == 'message_new' and id == 0: 
            import vk_api
            from vk_api.keyboard import VkKeyboard, VkKeyboardColor
            from vk_api.utils import get_random_id  
            info = ""    
            sql = "select id,info,data_id from setting where name = 'Токен' "
            cursor.execute(sql)
            data = cursor.fetchall()
            for rec in data: 
                id,info,data_id = rec.values() 
            if info != "":
                apikey_avtor = info
            vk_session = vk_api.VkApi(token=apikey_avtor)
            vk = vk_session.get_api()  
            info = "нет сообщения"    
            sql = "select id,info,data_id from setting where name = 'Нет сообщения' "
            cursor.execute(sql)
            data = cursor.fetchall()
            for rec in data: 
                id,info,data_id = rec.values() 
                message_out_min = info
                message_out     = info
            kb = ''    
            if message != '': 
                sql = "select id,info,data_id from message where name = 'Имя' and info = '{}' ".format (message)
                cursor.execute(sql)
                data = cursor.fetchall()
                data_id = 0
                for rec in data: 
                    id,info,data_id = rec.values() 
                message_info = {}    
                if data_id != 0:    
                    sql = "select id,name,info,data_id from message where data_id = {} ".format (data_id)
                    cursor.execute(sql)
                    data = cursor.fetchall()
                    for rec in data: 
                        id,name,info,data_id = rec.values() 
                        message_info[name] = info                    
                    message_out  = message_info.setdefault('Текст',message_out_min)                    
                    message_menu = message_info.setdefault('Меню','')
                    if message_menu != '':
                        sql = "select id,info,data_id from menu where name = 'Имя' and info = '{}' ".format (message_menu)
                        cursor.execute(sql)
                        data = cursor.fetchall()
                        data_id = 0
                        for rec in data: 
                            id,info,data_id = rec.values() 
                        menu_info = {}    
                        if data_id != 0:    
                            sql = "select id,name,info,data_id from menu where data_id = {} ".format (data_id)
                            cursor.execute(sql)
                            data = cursor.fetchall()
                            for rec in data: 
                                id,name,info,data_id = rec.values() 
                                menu_info[name] = info 
                            kb = 'Ok'
                            from vk_api.keyboard import VkKeyboard, VkKeyboardColor
                            keyboard = VkKeyboard(one_time=True)
                            if menu_info.setdefault('Кнопка 11','') != '':        
                                if menu_info.setdefault('Цвет 11','') == 'Белый':                             
                                    keyboard.add_button(menu_info.setdefault('Кнопка 11',''), color=VkKeyboardColor.SECONDARY)
                                if menu_info.setdefault('Цвет 11','') == 'Зеленый':                             
                                    keyboard.add_button(menu_info.setdefault('Кнопка 11',''), color=VkKeyboardColor.POSITIVE)
                            if menu_info.setdefault('Кнопка 12','') != '' :                                             
                                if menu_info.setdefault('Цвет 12','') == 'Белый':                             
                                    keyboard.add_button(menu_info.setdefault('Кнопка 12',''), color=VkKeyboardColor.SECONDARY)
                                if menu_info.setdefault('Цвет 12','') == 'Зеленый':                             
                                    keyboard.add_button(menu_info.setdefault('Кнопка 12',''), color=VkKeyboardColor.POSITIVE)
            if kb != '':
                vk.messages.send(peer_id=user_id,random_id=get_random_id(),message=message_out,keyboard=keyboard.get_keyboard()) 
            else:    
                vk.messages.send(peer_id=user_id,random_id=get_random_id(),message=message_out) 
    return 'ok'
 
@app.route('/cripta_command/<access_code>/', methods=["GET", "POST"])   ### <access_code>/<namebot>/
def cripta_command (access_code):     ### 
    if request.method == "POST":
        parsersring = request.json 
        print ('[parsersring]',parsersring)
        info     = parsersring.setdefault('Информация','')
        command  = parsersring.setdefault('Команда','')        
        print ('    [Команда]    :',command)
        print ('    [Информация] :',info)
        
        if command == 'Крипта : Получить билет fetchOHLCV':
            import iz_exchanges
            exchange    = info.setdefault('exchange','')
            pair        = info.setdefault('pair','') 
            timeframes  = info.setdefault('timefraim','') 
            limit       = info.setdefault('limit',1) 
            print ('[+]-----------------------------------[+]')
            print ('[+] exchange   :',exchange)
            print ('[+] pair       :',pair)
            print ('[+] timeframes :',timeframes)
            print ('[+] limit      :',limit)
            print ('[+]-----------------------------------[+]')
            answer = iz_exchanges.exchanges_fetchOHLCV (exchange,pair,timeframes,limit)
            print ('    [answer]',answer)
            return answer
            
        if command == 'Крипта : Получить список криптобирж':
            import iz_exchanges
            answer = iz_exchanges.exchanges_myexchange ()
            print ('    [answer]',answer)
            return answer
            
        if command == 'Крипта : Получить список инструментов fetchMarkets':    
            import iz_exchanges
            exchange = info.setdefault('exchange','')
            print ('[+]-----------------------------------[+]')
            print ('[+] exchange   :',exchange)
            print ('[+]-----------------------------------[+]')
            answer = iz_exchanges.exchanges_fetchMarkets (exchange)
            print ('    [answer]',answer)
            return answer            

        if command == 'Крипта : Получить баланс':  
            import iz_exchanges
            exchange = info.setdefault('exchange','')
            apiKey   = info.setdefault('apiKey','')
            secret   = info.setdefault('secret','')   
            spot     = info.setdefault('spot','spot')  
            print ('[+]-----------------------------------[+]')
            print ('[+] exchange   :',exchange)
            print ('[+] apiKey     :',apiKey)
            print ('[+] secret     :',secret)
            print ('[+] spot       :',spot)
            print ('[+]-----------------------------------[+]')
            answer = iz_exchanges.exchanges_fetchBalance (exchange,apiKey,secret,spot)
            print ('    [answer]',answer)                 
            return answer     
            
        if command == 'Крипта : Создать фьючерный ордер на покупку': ##long
            import iz_exchanges
            exchange = info.setdefault('exchange','')
            apiKey   = info.setdefault('apiKey','')
            secret   = info.setdefault('secret','')   
            amount   = info.setdefault('amount','')
            pair     = info.setdefault('pair','') 
            print ('[+]-----------------------------------[+]')
            print ('[+] exchange   :',exchange)
            print ('[+] apiKey     :',apiKey)
            print ('[+] secret     :',secret)
            print ('[+] amount     :',amount)
            print ('[+] pair       :',pair)
            print ('[+]-----------------------------------[+]')            
            answer = iz_exchanges.create_market_order_long (exchange,apiKey,secret,pair,amount)
            print ('    [answer]',answer)                   
            return answer  
            
        if command == 'Крипта : Создать фьючерный ордер на продажу': ##short
            import iz_exchanges
            exchange = info.setdefault('exchange','')
            apiKey   = info.setdefault('apiKey','')
            secret   = info.setdefault('secret','')   
            amount   = info.setdefault('amount','')
            pair     = info.setdefault('pair','') 
            print ('[+]-----------------------------------[+]')
            print ('[+] exchange   :',exchange)
            print ('[+] apiKey     :',apiKey)
            print ('[+] secret     :',secret)
            print ('[+] amount     :',amount)
            print ('[+] pair       :',pair)   
            print ('[+]-----------------------------------[+]')            
            answer = iz_exchanges.create_market_order_short (exchange,apiKey,secret,pair,amount)
            print ('    [answer]',answer)                    
            return answer  
            
        if command == 'Крипта : Выставить плечо':  
            import iz_exchanges
            exchange  = info.setdefault('exchange','')
            apiKey    = info.setdefault('apiKey','')
            secret    = info.setdefault('secret','')   
            leverage  = info.setdefault('leverage',0)  
            pair      = info.setdefault('pair','')
            print ('[+]-----------------------------------[+]')
            print ('[+] exchange   :',exchange)
            print ('[+] apiKey     :',apiKey)
            print ('[+] secret     :',secret)
            print ('[+] leverage   :',leverage)
            print ('[+] pair       :',pair)   
            print ('[+]-----------------------------------[+]')                        
            answer = iz_exchanges.set_leverage (exchange,apiKey,secret,pair,leverage)
            print ('    [answer]',answer)
            return answer     

        if command == 'Крипта : Получить позиции':  
            import iz_exchanges
            exchange  = info.setdefault('exchange','')
            apiKey    = info.setdefault('apiKey','')
            secret    = info.setdefault('secret','')   
            print ('[+]-----------------------------------[+]')
            print ('[+] exchange   :',exchange)
            print ('[+] apiKey     :',apiKey)
            print ('[+] secret     :',secret)
            print ('[+]-----------------------------------[+]')             
            answer = iz_exchanges.exchanges_fetch_positions (exchange,apiKey,secret)
            print ('    [answer]',answer)
            return answer     
           
        if command == 'Крипта : Получить load_markets':
            import iz_exchanges
            exchange = info.setdefault('exchange','')  
            print ('[+]-----------------------------------[+]')
            print ('[+] exchange   :',exchange)
            print ('[+]-----------------------------------[+]')                         
            answer = iz_exchanges.exchanges_loadMarkets (exchange)
            print ('    [answer]',answer)
            return answer      
                        
        if command == 'Крипта : Получить OrderBook':
            import iz_exchanges
            exchange = info.setdefault('exchange','')  
            pair     = info.setdefault('pair','')  
            print ('[+]-----------------------------------[+]')
            print ('[+] exchange   :',exchange)
            print ('[+] pair       :',pair)
            print ('[+]-----------------------------------[+]')                         
            answer = iz_exchanges.exchanges_fetchOrderBook (exchange,pair)
            print ('    [answer]',answer)
            return answer  
            
        if command == 'Крипта : Получить OrderBook':
            import iz_exchanges
            exchange = info.setdefault('exchange','')  
            pair     = info.setdefault('pair','')  
            print ('[+]-----------------------------------[+]')
            print ('[+] exchange   :',exchange)
            print ('[+] pair       :',pair)
            print ('[+]-----------------------------------[+]')          
            answer = iz_exchanges.exchanges_fetchOrderBook (exchange,pair)
            print ('    [answer]',answer)
            return answer  

        if command == 'Крипта : Создать лимитный ордер на покупку':
            import iz_exchanges
            exchange    = info.setdefault('exchange','')  
            apiKey      = info.setdefault('apiKey','')
            secret      = info.setdefault('secret','')  
            pair        = info.setdefault('pair','')              
            amount      = info.setdefault('amount','')
            price       = info.setdefault('price','')   
            print ('[+]-----------------------------------[+]')
            print ('[+] exchange   :',exchange)
            print ('[+] apiKey     :',apiKey)
            print ('[+] secret     :',secret)            
            print ('[+] pair       :',pair)
            print ('[+] amount     :',amount)
            print ('[+] price      :',price)
            print ('[+]-----------------------------------[+]')             
            answer = iz_exchanges.exchanges_createLimitBuyOrder (exchange,apiKey,secret,pair,amount,price)
            print ('    [answer]',answer)
            return answer  

        if command == 'Крипта : Создать лимитный ордер на продажу':
            import iz_exchanges
            exchange = info.setdefault('exchange','')  
            apiKey   = info.setdefault('apiKey','')
            secret   = info.setdefault('secret','')  
            pair     = info.setdefault('pair','')              
            amount   = info.setdefault('amount','')
            price    = info.setdefault('price','')   
            print ('[+]-----------------------------------[+]')
            print ('[+] exchange   :',exchange)
            print ('[+] apiKey     :',apiKey)
            print ('[+] secret     :',secret)            
            print ('[+] pair       :',pair)
            print ('[+] amount     :',amount)
            print ('[+] price      :',price)
            print ('[+]-----------------------------------[+]')             
            answer = iz_exchanges.exchanges_createLimitSellOrder (exchange,apiKey,secret,pair,amount,price)
            print ('    [answer]',answer)
            return answer  
         
        if command == 'Крипта : Список выставленных ордеров':
            import iz_exchanges
            exchange   = info.setdefault('exchange','')  
            apiKey     = info.setdefault('apiKey','')
            secret     = info.setdefault('secret','')  
            pair       = info.setdefault('pair','')              
            amount     = info.setdefault('amount','')
            price      = info.setdefault('price','')   
            print ('[+]-----------------------------------[+]')
            print ('[+] exchange   :',exchange)
            print ('[+] apiKey     :',apiKey)
            print ('[+] secret     :',secret)            
            print ('[+] pair       :',pair)
            print ('[+] amount     :',amount)
            print ('[+] price      :',price)
            print ('[+]-----------------------------------[+]')             
            answer = iz_exchanges.exchanges_fetchOpenOrders (exchange,apiKey,secret,pair)
            print ('    [answer]',answer)
            return answer  
            
        if command == 'Крипта : Показать статус ордера':
            import iz_exchanges
            exchange = info.setdefault('exchange','')  
            apiKey   = info.setdefault('apiKey','')
            secret   = info.setdefault('secret','')  
            pair     = info.setdefault('pair','')              
            ID       = info.setdefault('ID','')             
            print ('[+]-----------------------------------[+]')
            print ('[+] exchange   :',exchange)
            print ('[+] apiKey     :',apiKey)
            print ('[+] secret     :',secret)            
            print ('[+] pair       :',pair)
            print ('[+] ID         :',ID)
            print ('[+]-----------------------------------[+]')             
            answer = iz_exchanges.exchanges_fetchOrder (exchange,apiKey,secret,pair,ID)
            print ('    [answer]',answer)
            return answer             
              
        if command == 'Крипта : Удалить выставленный ордер':
            import iz_exchanges
            exchange = info.setdefault('exchange','')  
            apiKey   = info.setdefault('apiKey','')
            secret   = info.setdefault('secret','')  
            pair     = info.setdefault('pair','')    
            ID       = info.setdefault('ID','')            
            print ('[+]-----------------------------------[+]')
            print ('[+] exchange   :',exchange)
            print ('[+] apiKey     :',apiKey)
            print ('[+] secret     :',secret)            
            print ('[+] pair       :',pair)
            print ('[+] ID         :',ID)
            print ('[+]-----------------------------------[+]')             
            answer = iz_exchanges.exchanges_cancelOrder (exchange,apiKey,secret,ID,pair)
            print ('    [answer]',answer)
            return answer             
                  
        if command == 'Крипта : Цена покупки':
            import iz_exchanges
            exchange = info.setdefault('exchange','')
            pair     = info.setdefault('pair','')  
            print ('[+]-----------------------------------[+]')
            print ('[+] exchange   :',exchange)
            print ('[+] pair       :',pair)
            print ('[+]-----------------------------------[+]')              
            answer = iz_exchanges.exchanges_ask (exchange,pair)
            print ('    [answer]',answer)
            return answer    

        if command == 'Крипта : Цена продажи': 
            import iz_exchanges
            exchange = info.setdefault('exchange','')
            pair     = info.setdefault('pair','')  
            print ('[+]-----------------------------------[+]')
            print ('[+] exchange   :',exchange)
            print ('[+] pair       :',pair)
            print ('[+]-----------------------------------[+]')              
            answer = iz_exchanges.exchanges_bid (exchange,pair)
            print ('    [answer]',answer)
            return answer            
        return 'API'    

@app.route('/vk_command/<access_code>/', methods=["GET", "POST"])   ### <access_code>/<namebot>/
def vk_command (access_code):     ### 
    if request.method == "POST":
        parsersring = request.json 
        print ('[parsersring]',parsersring)
        info     = parsersring.setdefault('Информация','')
        command  = parsersring.setdefault('Команда','')        
        print ('    [Команда]    :',command)
        print ('    [Информация] :',info)

        if command == 'Боты : Получить users':
            import pymysql
            import json
            where    = info.setdefault('Условия','')                
            namebot = 'vk'            
            db = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database = namebot,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
            cursor = db.cursor()                                        
            sql = "select * from user_vk where "+str(where)+"".format ()
            cursor.execute(sql)
            data = cursor.fetchall()  
            json_string = json.dumps(data)
            return json_string
            
@app.route('/site_command/<access_code>/<command>/', methods=["GET", "POST"])   ### <access_code>/<namebot>/
def site_command (access_code,command):     ###
    import iz_bot
    import pymysql
    db = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database = 'A123_site',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    info = "Нет данных"
    id = 0
    sql = "select id,name,info from A_service where name = 'Задание' ORDER BY id DESC limit 1;".format ()
    cursor.execute(sql)
    results = cursor.fetchall()    
    for row in results:
        id,name,info = row.values() 
    element = {}    
    sql = "select id,name,info from A_service where data_id = {};".format (id)
    cursor.execute(sql)
    results = cursor.fetchall()    
    for row in results:
        id,name,info = row.values()
        element[name] = info    
        print ('[+] id,name,info',id,name,info)    
    answer = 'OK'
    namebot = '@'+str(element['Отправитель'])
    user_id = str(element['Получатель'])
    text    = str(element['Текст отправки'])
    send_data = {"Text":text,'Замена':[]}
    message_info = {'namebot':namebot,'user_id':user_id}
    answer = iz_bot.send_message (message_info,send_data)      
    return str(answer)

@app.route('/send_1c/<access_code>/', methods=["GET", "POST"])   ### <access_code>/<namebot>/
def send_1c (access_code):     ### 
    if request.method == "POST":
        parsersring = request.json 
        print ('[parsersring]',parsersring)
        print ('[parsed_string]:',parsersring) 
        info     = parsersring.setdefault('Информация','')
        command  = parsersring.setdefault('Команда','')        
        print ('[+] command:',command)

        if command == '1С : Информация':
            import requests
            user_id     = info.setdefault('user_id','399838806')
            token       = info.setdefault('token','6988761810:AAHsyODYS5qrJSmjbxaJs6JuAR0y2auZaYQ')
            message_out        = info.setdefault('message_out','test')  
            print ('[+] user_id',user_id)
            print ('[+] text',message_out)
            method = "sendMessage"
            params = {}
            params['chat_id'] = user_id                  
            params['text'] = message_out
            params['parse_mode'] = 'HTML'                
            url  = 'https://api.telegram.org/bot{0}/{1}'.format(token, method)
            resp = requests.post(url, params) 
            answer = resp.json()
            return str(answer)
            
        if command == '1С : Старт системы':
            import requests
            user_id     = info.setdefault('user_id','399838806')
            token       = info.setdefault('token','6988761810:AAHsyODYS5qrJSmjbxaJs6JuAR0y2auZaYQ')
            message_out         = info.setdefault ('message_out','test')  
            message_name        = info.setdefault('message_name','test')  
            print ('[+] user_id',user_id)
            print ('[+] text',message_out)
            method = "sendMessage"
            params = {}
            params['chat_id'] = user_id                  
            params['text'] = message_out
            params['parse_mode'] = 'HTML'                
            url  = 'https://api.telegram.org/bot{0}/{1}'.format(token, method)
            resp = requests.post(url, params) 
            answer = resp.json()
            return str(answer)            

@app.route('/bot_command/<access_code>/', methods=["GET", "POST"])   ### <access_code>/<namebot>/
def bot_command (access_code):     ### 
    if request.method == "POST":
        parsersring = request.json 
        print ('[parsersring]',parsersring)
        info     = parsersring.setdefault('Информация','')
        command  = parsersring.setdefault('Команда','')        
        print ('    [Команда]    :',command)
        print ('    [Информация] :',info)
        
        
        if command == 'Бот : Анкетирование':
            import json
            import pymysql
            namebot  = info.setdefault('namebot','Serofim_anketa_bot')
            name     = info.setdefault('name','')
            info_s   = info.setdefault('info','')
            data_id  = info.setdefault('data_id','')
            id       = info.setdefault('id','')
            print ('[+]-----------------------------------[+]')
            print ('[+] id      :',id)
            print ('[+] namebot :',namebot)
            print ('[+] name    :',name)
            print ('[+] info    :',info)
            print ('[+] data_id :',data_id)
            print ('[+]-----------------------------------[+]')
            db = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database = namebot,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
            cursor   = db.cursor()
            sql = "INSERT INTO `service` (`name`,`data_id`,`info`,`status`,`rating`) VALUES ('{}',{},'{}','{}',{})".format (name,data_id,info_s,'',0)
            print ('[sql] : ',sql)
            sql_save = ()
            cursor.execute(sql,sql_save)
            lastid = cursor.lastrowid 
            db.commit() 
            sql = "UPDATE service SET data_id = {} WHERE id = {} ".format (lastid,lastid)
            print ('[sql] : ',sql)
            cursor.execute(sql)
            db.commit()
            data = {'answer':lastid}
            json_string = json.dumps(lastid)
            print ('    [answer]',json_string)
            return str(answer)        
        
        if command == 'Бот : Список пользователей':
            import json
            namebot     = info.setdefault('namebot','')
            print ('[+]-----------------------------------[+]')
            print ('[+] namebot :',namebot)
            print ('[+]-----------------------------------[+]')            
            db,cursor = connect (namebot)            
            sql = "select id,name,info,data_id,status from users where name = 'user_id' ;".format ()
            print ('[sql] : ',sql)
            cursor.execute(sql)
            data = cursor.fetchall()
            json_string = json.dumps(data)
            print ('[answer]',json_string)
            return str(json_string)                           
        
        if command == 'Бот : Информация о пользователе':
            import json            
            namebot     = info.setdefault('namebot','')
            data_id     = info.setdefault('data_id','')            
            print ('[+]-----------------------------------[+]')
            print ('[+] namebot :',namebot)
            print ('[+] data_id :',data_id)
            print ('[+]-----------------------------------[+]')               
            db,cursor = connect (namebot)            
            sql = "select id,name,info,data_id,status from users where data_id = {} ;".format (data_id)
            print ('[sql] : ',sql)
            cursor.execute(sql)
            data = cursor.fetchall()
            json_string = json.dumps(data)
            print ('    [answer]',json_string)
            return str(json_string)        
               
        if command == 'Бот : Отправить сообщение':
            import json
            import requests
            user_id     = info.setdefault('user_id','')
            token       = info.setdefault('token','')
            message_out = info.setdefault('message_out','')
            print ('[+]-----------------------------------[+]')
            print ('[+] user_id :',user_id)
            print ('[+] token   :',token)
            print ('[+] text    :',message_out)
            print ('[+]-----------------------------------[+]')
            method = "sendMessage"
            params = {}
            params['chat_id'] = user_id                  
            params['text'] = message_out
            params['parse_mode'] = 'HTML'                
            url  = 'https://api.telegram.org/bot{0}/{1}'.format(token, method)
            resp = requests.post(url, params) 
            json_string = resp.json()
            print ('    [answer]',json_string)
            return str(json_string)        
        
        if command == 'Телеграм : Создать меню':
            import pymysql
            import json
            namebot     = info.setdefault('namebot','')
            text        = info.setdefault('Текст','')
            name_menu   = info.setdefault('Имя','')
            menu        = info.setdefault('Меню','') 
            type_m      = info.setdefault('Тип_кнопки','')            
            key11       = info.setdefault('Кнопка_11','')
            key12       = info.setdefault('Кнопка_12','')
            key13       = info.setdefault('Кнопка_13','')
            key21       = info.setdefault('Кнопка_21','')
            key22       = info.setdefault('Кнопка_22','')
            key23       = info.setdefault('Кнопка_23','')
            print ('[+]-----------------------------------[+]')
            print ('[+] namebot   :',namebot)
            print ('[+] name_menu :',name_menu)
            print ('[+] text      :',text)
            print ('[+]-----------------------------------[+]')            
            db,cursor = connect (namebot)  
            data_id = 0
            sql = "select id,data_id from menu  where name = 'Имя' and info = '{}' limit 1;".format (name_menu)
            print ('[sql] : ',sql)
            cursor.execute(sql)
            data = cursor.fetchall()
            for rec in data: 
                id,data_id  =  rec.values()
            #data = 'OK'    
            #json_string = json.dumps(data)
            #print ('    [answer]',json_string)
            #return str(json_string)     
            ########################################################################################################################################
            id = 0
            sql = "select id,name from menu  where name = 'Имя' and data_id = '{}' limit 1;".format (data_id)
            cursor.execute(sql)
            data = cursor.fetchall()
            for rec in data: 
                id,name  =  rec.values()    
            if id == 0:
                sql = "INSERT INTO `menu` (`name`,`data_id`,`info`,`status`) VALUES ('{}',{},'{}','{}')".format ('Имя',data_id,name_menu,'')
                sql_save = ()
                cursor.execute(sql,sql_save)
                lastid = cursor.lastrowid 
                db.commit()            
            else:    
                sql = "UPDATE menu SET `info` = '{}' WHERE name = 'Имя' and data_id = {} ".format (name_menu,data_id)
                sql_save = ()
                cursor.execute(sql,sql_save)  
                db.commit()      
            update_key ('Кнопка 11','Замена 11',key11,data_id,namebot)   
            update_key ('Кнопка 21','Замена 21',key21,data_id,namebot)            
            update_key ('Кнопка 22','Замена 22',key22,data_id,namebot)            
            update_key ('Кнопка 23','Замена 23',key23,data_id,namebot)            
            data = {'answer':'OK'}
            json_string = json.dumps(data)
            print ('    [answer]',json_string)
            return str(json_string)
        
        if command == 'Телеграм : Записать сообшение':
            import json
            namebot     = info.setdefault('namebot','')
            text        = info.setdefault('Текст','')
            name        = info.setdefault('Имя','')
            menu        = info.setdefault('Меню','')
            print ('[+]-----------------------------------[+]')
            print ('[+] namebot   :',namebot)
            print ('[+] name      :',name_menu)
            print ('[+] text      :',text)
            print ('[+] menu      :',menu)
            print ('[+]-----------------------------------[+]')               
            db,cursor = connect (namebot)            
            data_id = 0
            sql = "select id,data_id from message  where name = 'Имя' and info = '{}' limit 1;".format (name)
            cursor.execute(sql)
            data = cursor.fetchall()
            for rec in data: 
                id,data_id  =  rec.values()
            if data_id == 0: 
                sql = "INSERT INTO message (name,data_id,info,status) VALUES (%s,%s,%s,%s)".format ()
                sql_save = ('Имя',0,name,'')
                cursor.execute(sql,sql_save)
                lastid = cursor.lastrowid   
                db.commit()
                data_id = lastid
                sql = "UPDATE message SET `data_id` = {} WHERE id = {} ".format (data_id,data_id)
                sql_save = ()
                cursor.execute(sql,sql_save)  
                db.commit()  
                sql = "INSERT INTO message (name,data_id,info,status) VALUES (%s,%s,%s,%s)".format ()
                sql_save = ('Текст',data_id,text,'')
                cursor.execute(sql,sql_save)
                lastid = cursor.lastrowid   
                db.commit()
            else:
                sql = "UPDATE message SET `info` = '{}' WHERE name = 'Текст' and data_id = {} ".format (text,data_id)
                sql_save = ()
                cursor.execute(sql,sql_save)  
                db.commit()  
                sql = "UPDATE message SET `info` = '{}' WHERE name = 'Меню' and data_id = {} ".format (menu,data_id)
                sql_save = ()
                cursor.execute(sql,sql_save)  
                db.commit() 
                data = {'answer':'OK'}
            json_string = json.dumps(data)
            print (json_string)
            return str(json_string)    

        if command == 'Телеграм : Сменить пароль':
            import random
            db,cursor = connect ("A123_site")
            namebot     = info.setdefault('namebot','')
            user_id     = info.setdefault('user_id','')
            print ('[+]-----------------------------------[+]')
            print ('[+] namebot :',namebot)
            print ('[+] user_id :',user_id)
            print ('[+]-----------------------------------[+]')            
            ps = ''
            strSM = "01234567890QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvnm"
            for number1 in range(5):
                for number2 in range(4):
                    rn = random.randint(0,len(strSM))
                    ps = ps + strSM[rn:rn+1]
                ps = ps + '-' 
                for number2 in range(4):
                    rn = random.randint(0,len(strSM))
                    ps = ps + strSM[rn:rn+1]   
            password = ps
            sql = "UPDATE access SET `pass` = '{}' WHERE namebot = '{}' and user_id = '{}' ".format (password,namebot,user_id)
            sql_save = ()
            cursor.execute(sql,sql_save)  
            db.commit()  
            data = {'answer':password}            
            json_string = json.dumps(data)
            print (json_string)
            return str(json_string)     
                            
        if command == 'Телеграм : Получить пароль':
            import json
            import pymysql
            import random
            namebot     = info.setdefault('namebot','')
            user_id     = info.setdefault('user_id','')
            print ('[+]-----------------------------------[+]')
            print ('[+] namebot :',namebot)
            print ('[+] user_id :',user_id)
            print ('[+]-----------------------------------[+]')              
            db,cursor = connect ("A123_site")
            sql = "select id,pass from access  where namebot = '{}' and user_id = '{}' limit 1;".format (namebot,user_id)
            cursor.execute(sql)
            data = cursor.fetchall()
            elements = []
            password = ''
            for rec in data: 
                id,password  =  rec.values()
            if password == '':
                ps = ''
                strSM = "01234567890QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvnm"
                for number1 in range(5):
                    for number2 in range(4):
                        rn = random.randint(0,len(strSM))
                        ps = ps + strSM[rn:rn+1]
                    ps = ps + '-' 
                    for number2 in range(4):
                        rn = random.randint(0,len(strSM))
                        ps = ps + strSM[rn:rn+1]   
                password = ps
                sql = "INSERT INTO `access` (`name`,`user_id`,`table`,`namebot`,`pass`) VALUES (%s,%s,%s,%s,%s)"
                sql_save = ('Администрирование',user_id,'info',namebot,password)
                cursor.execute(sql,sql_save)
                lastid = cursor.lastrowid
                db.commit()
            data = {'answer':password}            
            json_string = json.dumps(data)
            print ('    [answer]',json_string)
            return str(json_string)             

        if command == 'Телеграм : Открыть доступ':
            import json
            namebot     = info.setdefault('namebot','')
            user_id     = info.setdefault('user_id','')
            name        = info.setdefault('name','')
            acces       = info.setdefault('Доступ','')
            name_eng    = info.setdefault('name_end','')
            print ('[+]-----------------------------------[+]')
            print ('[+] namebot :',namebot)
            print ('[+] user_id :',user_id)
            print ('[+] name    :',name)
            print ('[+] acces   :',acces)
            print ('[+]-----------------------------------[+]')             
            db,cursor = connect ("A123_site")
            sql = "INSERT INTO security (`name`,`user_id`,`status`,`menu`,`namebot`) VALUES (%s,%s,%s,%s,%s)"
            sql_save = (name_eng,user_id,acces,name,namebot)
            cursor.execute(sql,sql_save)
            lastid = cursor.lastrowid
            db.commit()
            data = {'answer':lastid}            
            json_string = json.dumps(data)
            print ('    [answer]',json_string)
            return str(json_string) 
        
        if command == 'Телеграм : Список ботов':
            import json
            namebot = 'bot_main'
            print ('[+]-----------------------------------[+]')
            print ('[+]-----------------------------------[+]')               
            db,cursor = connect (namebot)
            sql = "select id,name from bot_bots  where 1=1;".format ()
            cursor.execute(sql)
            data = cursor.fetchall()
            elements = []
            for rec in data: 
                id,name  =  rec.values()
                elements.append ([id,name])
            json_string = json.dumps(elements)
            print ('    [answer]',json_string)
            return json_string
        
        if command == 'Телеграм : Отправить сообщение по токену':
            import requests
            user_id     = info.setdefault('user_id','')
            token       = info.setdefault('token','')
            message_out = info.setdefault('message_out','')  
            print ('[+]-----------------------------------[+]')
            print ('[+] user_id    :',user_id)
            print ('[+] token      :',name)
            print ('[+] message_out:',message_out)
            print ('[+]-----------------------------------[+]')   
            method = "sendMessage"
            params = {}
            params['chat_id'] = user_id                  
            params['text'] = message_out
            params['parse_mode'] = 'HTML'                
            url  = 'https://api.telegram.org/bot{0}/{1}'.format(token, method)
            resp = requests.post(url, params) 
            json_string = resp.json()
            print ('    [answer]',json_string)
            return str(answer)
                       
        if command == 'Боты : Отправить сообщение':
            import pymysql
            import iz_bot
            namebot     = info.setdefault('namebot','')                
            id_message  = info.setdefault('data_id','')
            text        = info.setdefault('text','')  
            menu        = info.setdefault('menu','')
            user_id     = info.setdefault('user_id','')
            no_save     = info.setdefault('no_save','')           
            print ('[+]-----------------------------------[+]')
            print ('[+] user_id    :',user_id)
            print ('[+] menu       :',menu)
            print ('[+] text       :',text)
            print ('[+]-----------------------------------[+]')               
            db,cursor = connect (namebot)
            zamena = {}
            send_data = {"Text":text,'Замена':zamena}
            if no_save == 'Yes':
                send_data['Запись в базу '] = 'Не записывать'
            message_info = {'namebot':namebot,'user_id':user_id,'Меню':'Кнопка запуска меню'}
            json_string  = iz_bot.send_message (message_info,send_data) 
            print ('    [answer]',json_string)            
            return str(answer)
               
        if command == 'Боты : Создать service':
            import pymysql
            namebot    = info.setdefault('namebot','')                
            data_id    = info.setdefault('data_id','')
            name       = info.setdefault('name','')  
            info       = info.setdefault('info','')   
            print ('[+]-----------------------------------[+]')
            print ('[+] namebot    :',namebot)
            print ('[+] data_id    :',data_id)
            print ('[+] name       :',name)
            print ('[+] info       :',info)
            print ('[+]-----------------------------------[+]')    
            db = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database = namebot,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
            cursor = db.cursor()                                        
            sql = "INSERT INTO service (name,data_id,info,status,rating) VALUES (%s,%s,%s,%s,%s)".format ()
            sql_save = (name,data_id,info,'',0)
            cursor.execute(sql,sql_save)
            db.commit()
            lastid = cursor.lastrowid 
            data = {'answer':lastid} 
            json_string = json.dumps(data)
            print ('    [answer]',json_string)
            return str(json_string) 
        
        if command == 'Боты : получить FTP':
            import ftplib
            import json
            NameFile    = info.setdefault('Имя','')
            print ('[+]-----------------------------------[+]')
            print ('[+] NameFile    :',NameFile)
            print ('[+]-----------------------------------[+]')    
            host            = "192.168.1.237"
            ftp_user        = "admin"
            ftp_password    = "podkjf4"
            server= ftplib.FTP(host, ftp_user, ftp_password)
            print("[+] ... CONNECTED TO FTP")
            files = server.nlst(NameFile)  #"/Public/bot_data/audiobooks_314_bot/Best/MDS/mBooks/"
            json_string = json.dumps(files)
            print ('    [answer]',json_string)
            return json_string
                    
        if command == 'Боты : получить размер':
            import ftplib
            import json
            NameFile    = info.setdefault('Имя','')
            print ('[+]-----------------------------------[+]')
            print ('[+] NameFile    :',NameFile)
            print ('[+]-----------------------------------[+]')   
            host            = "192.168.1.237"
            ftp_user        = "admin"
            ftp_password    = "podkjf4"
            filename        = NameFile
            server= ftplib.FTP(host, ftp_user, ftp_password)
            print("[+] ... CONNECTED TO FTP")
            try:
                files = str (server.size(NameFile)) 
            except :
                files = str ("Каталог")
            json_string = json.dumps(files)
            print ('    [answer]',json_string)
            return json_string    
                
        if command == 'Боты : Создать сообшение отправки':
            import pymysql
            import json
            namebot = info.setdefault('namebot','')                
            name    = info.setdefault('Имя','')
            text    = info.setdefault('Текст','')            
            menu    = info.setdefault('Меню','') 
            print ('[+]-----------------------------------[+]')
            print ('[+] namebot    :',namebot)
            print ('[+] Имя        :',name)
            print ('[+] Меню       :',menu)
            print ('[+] Текст      :',text)
            print ('[+]-----------------------------------[+]')   
            db = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database = namebot,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
            cursor = db.cursor()                                        
            sql = "INSERT INTO message (name,data_id,info,status) VALUES ('Имя',0,'{}','')".format (name)
            cursor.execute(sql)
            db.commit() 
            lastid = cursor.lastrowid
            sql = "UPDATE message SET data_id = '{}' WHERE id = {}  ".format(lastid,lastid)
            cursor.execute(sql)
            db.commit()
            sql = "INSERT INTO message (name,data_id,info,status) VALUES ('Текст',{},'{}','')".format (lastid,text)
            cursor.execute(sql)
            db.commit() 
            sql = "INSERT INTO message (name,data_id,info,status) VALUES ('Меню',{},'{}','')".format (lastid,menu)
            cursor.execute(sql)
            db.commit() 
            data = {'answer':lastid}
            json_string = json.dumps(data)
            print ('    [answer]',json_string)            
            return str(json_string)

        if command == 'Боты : Создать обеденное меню':
            import pymysql
            namebot     = info.setdefault('namebot','')
            Assortment  = info.setdefault('Aссортимент','')
            Date        = info.setdefault('Дата','')
            name        = info.setdefault('Наименование','')
            menu01 = info.setdefault('Меню01','')
            menu11 = info.setdefault('Меню11','')
            menu02 = info.setdefault('Меню02','')
            menu21 = info.setdefault('Меню21','')
            menu03 = info.setdefault('Меню03','')
            menu31 = info.setdefault('Меню31','')
            menu04 = info.setdefault('Меню04','')
            menu41 = info.setdefault('Меню41','')
            print ('[+]-----------------------------------[+]')
            print ('[+] namebot     :',namebot)
            print ('[+] Aссортимент :',name)
            print ('[+] Дата        :',Date)
            print ('[+] Наименование:',name)
            print ('[+]-----------------------------------[+]')             
            db = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database = namebot,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
            cursor = db.cursor()                
            sql = "INSERT INTO task (name,data_id,info,status) VALUES ('Aссортимент',0,'{}','')".format (Assortment)
            cursor.execute(sql)
            db.commit() 
            lastid = cursor.lastrowid
            sql = "UPDATE task SET data_id = '{}' WHERE id = {}  ".format(lastid,lastid)
            cursor.execute(sql)
            db.commit()
            sql = "INSERT INTO task (name,data_id,info,status) VALUES ('{}',{},'{}','')".format ('Дата',lastid,Date,'')
            cursor.execute(sql)
            db.commit() 
            sql = "INSERT INTO task (name,data_id,info,status) VALUES ('{}',{},'{}','')".format ('Наименование',lastid,name,'')
            cursor.execute(sql)
            db.commit() 
            sql = "INSERT INTO task (name,data_id,info,status) VALUES ('{}',{},'{}','')".format ('menu01',lastid,menu01,'')
            cursor.execute(sql)
            db.commit() 
            sql = "INSERT INTO task (name,data_id,info,status) VALUES ('{}',{},'{}','')".format ('menu11',lastid,menu11,'')
            cursor.execute(sql)
            db.commit() 
            sql = "INSERT INTO task (name,data_id,info,status) VALUES ('{}',{},'{}','')".format ('menu02',lastid,menu02,'')
            cursor.execute(sql)
            db.commit() 
            sql = "INSERT INTO task (name,data_id,info,status) VALUES ('{}',{},'{}','')".format ('menu21',lastid,menu21,'')
            cursor.execute(sql)
            db.commit() 
            sql = "INSERT INTO task (name,data_id,info,status) VALUES ('{}',{},'{}','')".format ('menu03',lastid,menu03,'')
            cursor.execute(sql)
            db.commit() 
            sql = "INSERT INTO task (name,data_id,info,status) VALUES ('{}',{},'{}','')".format ('menu31',lastid,menu31,'')
            cursor.execute(sql)
            db.commit()             
            sql = "INSERT INTO task (name,data_id,info,status) VALUES ('{}',{},'{}','')".format ('menu04',lastid,menu04,'')
            cursor.execute(sql)
            db.commit()
            sql = "INSERT INTO task (name,data_id,info,status) VALUES ('{}',{},'{}','')".format ('menu41',lastid,menu41,'')
            cursor.execute(sql)
            db.commit() 
            data = {'answer':lastid}  
            json_string = json.dumps(data)
            print ('    [answer]',json_string)            
            return str(json_string)            

        if command == 'Боты : Удалить сообщение':
            import pymysql
            namebot = info.setdefault('namebot','')
            data_id = info.setdefault('data_id','0')
            print ('[+]-----------------------------------[+]')
            print ('[+] namebot     :',namebot)
            print ('[+] data_id     :',data_id)
            print ('[+]-----------------------------------[+]')             
            db = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database = namebot,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
            cursor = db.cursor()                
            sql = "UPDATE message SET status = 'delete' WHERE  data_id = '{}' ".format (data_id)
            cursor.execute(sql)
            db.commit()
            data = {'answer':'API'}  
            json_string = json.dumps(data)
            print ('    [answer]',json_string)            
            return str(json_string)            

        if command == 'Боты : Записать настройки':
            import pymysql
            namebot = info.setdefault('namebot','')
            data_id = info.setdefault('data_id','0')
            name    = info.setdefault('name','')
            info    = info.setdefault('info','')
            print ('[+]-----------------------------------[+]')
            print ('[+] namebot     :',namebot)
            print ('[+] data_id     :',data_id)
            print ('[+] name        :',name)
            print ('[+] info        :',info)
            print ('[+]-----------------------------------[+]')             
            db = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database = namebot,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
            cursor = db.cursor()                
            sql = "UPDATE setting SET info = '{}' WHERE  name = '{}' ".format (info,name)
            cursor.execute(sql)
            db.commit()
            data = {'answer':'API'}  
            json_string = json.dumps(data)
            print ('    [answer]',json_string)            
            return str(json_string)        
                        
        if command == 'Сайты : Получить Title':
            import pymysql
            import json
            sql = info.setdefault('sql','')
            print ('[+]-----------------------------------[+]')
            print ('[+] sql     :',sql)
            print ('[+]-----------------------------------[+]')              
            base = "site_rus"
            db = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database=base,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)        
            cursor = db.cursor()                    
            cursor.execute(sql)            
            data = cursor.fetchall()    
            json_string = json.dumps(data)
            print ('    [answer]',json_string)   
            return json_string    
   
        if command == 'Боты : Выполнить запрос':
            import pymysql
            import json
            namebot = info.setdefault('namebot','')
            sql     = info.setdefault('sql','')
            print ('[+]-----------------------------------[+]')
            print ('[+] namebot     :',namebot)
            print ('[+] sql     :',sql)
            print ('[+]-----------------------------------[+]')                          
            db = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database = namebot,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)            
            cursor = db.cursor() 
            cursor.execute(sql)
            data = cursor.fetchall()
            json_string = json.dumps(data)
            print ('    [answer]',json_string)   
            return json_string
            
        if command == 'Боты : Записать параметр пользователя':
            import pymysql
            import json
            namebot     = info.setdefault('namebot','')
            name_save   = info.setdefault('name','')
            info_save   = info.setdefault('info','')
            user_id     = info.setdefault('user_id','')
            print ('[+]-----------------------------------[+]')
            print ('[+] namebot     :',namebot)
            print ('[+] name_save   :',name_save)
            print ('[+] info_save   :',info_save)
            print ('[+] user_id     :',user_id)
            print ('[+]-----------------------------------[+]')              
            db = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database = namebot,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)            
            cursor = db.cursor() 
            sql = "select id,name,info,data_id from users where name = 'user_id' and info = '{}'".format (user_id)
            cursor.execute(sql)
            data = cursor.fetchall()  
            data_id = 0            
            for rec in data:
                id,name,info,data_id = rec.values()
                sql = "select id,name,info,data_id from users where name = '{}' and data_id = '{}'".format (name_save,id)
                cursor.execute(sql)
                data_find = cursor.fetchall()  
                id_find = 0            
                for rec_find in data_find:
                    id_find,name_find,info_find,data_id_find = rec_find.values()
                if id_find == 0:
                    sql = "INSERT INTO users (`name`,`info`,`data_id`,`status`) VALUES ('{}','{}',{},'{}')".format(name_save,info_save,id,'')
                    cursor.execute(sql)
                    db.commit()
                sql = "UPDATE users SET info = '{}' WHERE name = '{}' and data_id = '{}' ".format (info_save,name_save,id)
                cursor.execute(sql)
                db.commit()
            json_string = json.dumps(data)
            print ('    [answer]',json_string)            
            return str(json_string)                  
      
        if command == 'Телеграмм боты : Получить список анкет':
            import pymysql
            import json
            print ('[+]-----------------------------------[+]')
            print ('[+]-----------------------------------[+]')              
            base = "TemplateIzBot"
            db = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database=base,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)        
            cursor = db.cursor()                    
            sql = "select id,user_id,name01,name02,name03,name04,name05,name06,name07,name08,name09,name10,name11,name12,name13 from anketa where 1=1 "
            cursor.execute(sql)
            results = cursor.fetchall()   
            json_string = json.dumps(results)
            print ('    [answer]',json_string)   
            return str(json_string)   
               
        if command == 'Телеграмм боты : Получить информацию пользователя':
            print ('[+] Телеграмм боты : Получить информацию пользователя')
            import pymysql
            import json
            user_id = info.setdefault('user_id','')
            print ('[+]-----------------------------------[+]')
            print ('[+] user_id     :',user_id)
            print ('[+]-----------------------------------[+]')              
            base = "TemplateIzBot"
            db = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database=base,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)        
            cursor = db.cursor()                    
            sql = "select u1.id,u2.name,u2.info from users as u1, users as u2  where (u1.name = 'user_id' and u1.info = '{}') and u2.data_id = u1.id;".format(user_id)
            cursor.execute(sql)
            results = cursor.fetchall()   
            json_string = json.dumps(results)
            print ('    [answer]',json_string)   
            return json_string   
         
@app.route('/platon/<access_code>/', methods=["GET", "POST"])   ### Для Маруси навыки
def platon (access_code):     ###       
    import json
    if request.method == "POST":
        request_message = request.json 
        derived_session_fields = ['session_id', 'user_id', 'message_id']
        response_message = {
            "response": {
            "text": 'Платон молодец',
            "tts": 'Люба самый красивый человек на свете. Высылаем ей игрушки которые она заказала. А так же вкусняшки и подарки. Люба молодец',
            "end_session": False
            },
            "session": {derived_key: request_message['session'][derived_key] for derived_key in derived_session_fields},
            "version": request_message['version']
        }    
    json_string = response_message
    return json_string   
       
@app.route('/proxy/<name>/', methods=["GET", "POST"])   ### <access_code>/<namebot>/
def proxy (name):     ### 
    import pymysql
    import time
    base = 'nnmclub314_bot'
    db = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database=base,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)        
    cursor = db.cursor()                    
    sql = "select id,line from proxy where line = '{}' limit 1".format (name)
    cursor.execute(sql)
    results = cursor.fetchall()   
    id = 0
    for row in results:
        id,line = row.values()   
        print ('[line]',line)
    if id == 0:
        answer = 'save'    
        datatime = int(time.time())
        sql = "INSERT INTO proxy (`ip`,`port`,`type`,`status`,`line`,`datatime`) VALUES ('',0,'','','{}',{})".format (name,datatime)
        cursor.execute(sql)
        db.commit()
    else:
        answer = 'no'    
    return answer

@app.route('/')
def hello_world():
    return 'API'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3140)

