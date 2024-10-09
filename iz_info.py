

def connect (setting):
    #print ('[connect_info]',connect_info)
    import pymysql 
    db = pymysql.connect(host=connect_info['host'],user=connect_info['user'],password=connect_info['password'],database=connect_info['database'],charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)  
    cursor = db.cursor() 
    return db,cursor

def send_message (info,setting):
    import iz_bot
    import datetime
    name   = info.setdefault('Имя','')
    change = info.setdefault('Замена',[])    
    message_info = {'namebot':'@info314_bot'}
    send_data    = {'Text':name,'user_id':'399838806'}
    #connect_info = info.setdefault('connect_info','')
    #sql = info.setdefault('sql','')    
    #if sql != '':
    #    db,cursor = connect (connect_info)
    #    sql = sql
    #    cursor.execute(sql)
    #    results = cursor.fetchall() 
    #    print ('[results]',results)
    #    COUNT = results[0]['COUNT(*)']
    #    change.append (['#Колличество#',COUNT])    
    now = datetime.datetime.now()
    time_send = now.strftime("%d-%m-%Y %H:%M")    
    change.append (['#Время#',time_send])
    send_data['Замена'] = change
    print ('[+] message_info:',message_info)
    answer = iz_bot.send_message (message_info,send_data)
    
     