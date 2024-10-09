




if 1==1:
    import iz_bot
    import random
    import time
    namebot = 'ping314_bot'
    db,cursor = iz_bot.connect (namebot)   
    sql = "select id,name from task where status = '' and `type` = 'katalog ' "
    cursor.execute(sql)
    data = cursor.fetchall()
    random.shuffle(data)
    tasks = data
    
    list_phone_number = [{'name':'+79033671563','id':369}]
    random.shuffle(list_phone_number) 
    phone_number = list_phone_number[0]
    setting  = iz_bot.get_setting ({'namebot':'@info314_bot'})
    api_id   = int(setting.setdefault('api_id',192804))      #192804
    api_hash = str(setting.setdefault('api_hash','1b40d1d01f8922b384d44e29d32f6acf'))   #'1b40d1d01f8922b384d44e29d32f6acf'
    client_79033671563,answer = telegram_connect (phone_number,api_id,api_hash) 

    for task in tasks:
        print ('[+] task:',task)        
        answer  = client_79033671563.get_entity(task['name'])
        #print ('[+] answer',answer)
        print ('[+] answer',answer.title)
        time.sleep (2)
