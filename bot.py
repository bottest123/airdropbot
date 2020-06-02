from pyrogram import *
from captcha.image import ImageCaptcha
import string
import random
import tweepy
from datetime import datetime
from threading import Thread
from my import *
import logging as py_log
import csv

py_log.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=py_log.INFO)
logger = py_log.getLogger()
logger.setLevel(py_log.INFO)

start = start = datetime(year=2020, month=1, day=1)
stop = datetime(year=datetime.now().year,month=datetime.now().month,day=datetime.now().day)

app = Client('airdropbot')

#https://docs.pyrogram.org/api/methods/get_chat_members.html#pyrogram.Client.get_chat_members


image = ImageCaptcha(fonts=[captcha.ttf])
medalte_group = -1001468866458
medalte_channel = -1001170837570

#medalte_group = -370210522
#medalte_channel = -1001379057229

states = {}
captchas = {}
userinfo = {}
medium_sid = '1:zW7MfCv7K6PAZQi0tavnZJBQQOBs+7oGVgaxEd27fY4PUBk/TjLSIc0Cl3BCDqFT'
medium_uid = 'e0b92752ccdb'
twitter_api_key = '18rBpGEI7hKA6MK4wqpPE69Zc'
twitter_api_secret_key = 'wEqWBRnFA3YXRsCKw4xsbzQNl13vuIcViBbn43ZzCNOycMzd4K'

twitter_access_token = '1265070033769824261-xYBpXhLcVQjkaxaeCt1TOLSB6ifri5'
twitter_access_token_secret = 'boDnWE1zEXDKPT4tllKHktovbwNKrbVJ4eE25o3ypfLkY'

auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_secret_key)
auth.set_access_token(twitter_access_token, twitter_access_token_secret)
api = tweepy.API(auth)

def randomString(stringLength=5):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def gen_captcha(userid):
    string = randomString()
    data = image.generate(string)
    image.write(string, './captcha/{}.png'.format(str(userid)))
    states[str(userid)+'_captcha'] = string
    print(states[str(userid)+'_captcha'])


def captcha_query(_,message):
    user_id = message.from_user.id
    try:
        a = states[str(user_id)] == 'captcha_true'
    except:
        a = 0
    if a:
        return True

def tg_verify_query(_,query):
    a = query.data
    if 'verify_tg' in a:
        return True 
    else:
        return False
    
def twitter_verify_query(_,query):
    pass

def medium_verify_query(_,query):
    a = query.data
    if 'medium_verify' in a:
        return True
    else:
        return False

def medium_verify_time(_,query):
    a = query.data
    if 'verify_medium_time' in a:
        return True
    else:
        return False

def show_menu(_,query):
    a = query.data
    if a == 'show_menu':
        return True
    else:
        return False
    
def check_bal(_,query):
    a = query.data
    if 'show_balance' in a:
        return True
    else:
        return False

def check_ref(_,query):
    a = query.data
    if a == 'show_referral':
        return True
    else:
        return False

def twitter_verify_(_,query):
    a = query.data
    if 'twitter_verify' in a:
        return True
    else:
        return False

def twitter_input_query(client,message):
    user_id = message.from_user.id
    print(user_id)
    print(states[str(user_id)])
    try:
        state = states[str(user_id)]
    except:
        state = 'None'
    print('State =',state )
    if state == 'twitter_input':
        return True
    else:
        return False

def show_referral(_,query):
    a = query.data
    if 'show_referral' in a:
        return True
    else:
        return False

def show_menu_query(_,query):
    a = query.data
    if 'show_menu' in a:
        return True
    else:
        return False

captcha_filter = Filters.create(captcha_query)
tg_verify_filter = Filters.create(tg_verify_query)
medium_verify_filter  = Filters.create(medium_verify_query)
medium_verify_time_filter = Filters.create(medium_verify_time)
menu_filter = Filters.create(show_menu)
balance_filter = Filters.create(check_bal)
referral_filter= Filters.create(check_ref)
twitter_verify_filter = Filters.create(twitter_verify_)
twitter_input_filter = Filters.create(twitter_input_query)
show_referral_query = Filters.create(show_referral)
show_menu_filter = Filters.create(show_menu_query)
#token="1200128287:AAHr-j4Z8mFStSL5tX208gLLMPeXYdRTxno"


@app.on_message(Filters.command('start'))
def start(client,message):
    user_id  = message.from_user.id
    chat_id = message.chat['id']
    try:
        rreffid = int(message.text.split(" ",1)[1])
        rreff = True
    except:
        rreff = False
    try:
        level = userinfo[str(user_id)+'_task_level']
    except:
        user = check_user(user_id)
        if user:
            level = user[5]
            userinfo[str(user_id)+'_task_level'] = level
        else:
            if rreff:
                create_user(user_id,rreffid)
                new_ref(rreffid,user_id)
                try:
                    balance = userinfo[str(rreffid)+'_balance'] 
                except:
                    user = check_user(rreffid)
                    balance = user[5]
                balance = balance + 5
                update_user(rreffid,balance,'n','n','n')
                userinfo[str(rreffid)+'_balance'] = balance
                app.send_message(chat_id = rreffid,text = 'Congrats you have a referral and have got 5 MTDL tokens!')
                userinfo[str(user_id)+'_task_level'] = 1
                userinfo[str(user_id)+'_total_referrals'] = 0
            else:
                create_user(user_id,'n')
                userinfo[str(user_id)+'_task_level'] = 1
                userinfo[str(user_id)+'_total_referrals'] = 0
            user = check_user(user_id)
            level = user[5]
            userinfo[str(user_id)+'_task_level'] = level
    firstname = app.get_users(user_id).first_name
    if level == 1:
        message.reply('Hello [{}](tg://user?id={}),\nTo continue please solve the captcha below!'.format(firstname,user_id))
        gen_captcha(user_id)
        app.send_photo(chat_id = chat_id,photo = './captcha/{}.png'.format(str(user_id)))
        states[str(user_id)] = 'captcha_true'        
    elif level == 2:
        keyboard = [[InlineKeyboardButton("Join Group", url = 'https://t.me/medalte')],
                        [InlineKeyboardButton('Join Channel', url = 'https://t.me/medalteAnn')],
                        [InlineKeyboardButton('Done!', callback_data = 'verify_tg:{}'.format(user_id))]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message.reply('To be able to participate in the AirDrop you need to complete some tasks.\n\n Firstly join @medalte and @medalteAnn',reply_markup = reply_markup)
    elif level == 3:
        states[str(user_id)] = 'twitter_input'
        keyboard = [[InlineKeyboardButton('Visit Our twitter Page',url = 'https://twitter.com/medaltetoken')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message.reply('The next task is to visit our twitter profile and follow us,retweet and share our pinned post \nThen Send your username to me without @',reply_markup = reply_markup)
    elif level == 4:
        
        states[str(user_id)] = 'medium_wait_13'
        def change_wait_time(userid):
            import time
            n = 12
            while n >= 0:
                time.sleep(1)
                states[str(userid)] = 'medium_wait_{}'.format(n)
                n = n-1
        t = Thread(target = change_wait_time,args=(user_id,))
        t.start()
        keyboard = [[InlineKeyboardButton('Our medium page!',url = 'https://medium.com/@support_28864')],
            [InlineKeyboardButton("Done!", callback_data = 'verify_medium_time')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message.reply('Now visit our medium page and like/clap on any one of our posts!',reply_markup  = reply_markup)
    elif level == 5:
        keyboard = [[InlineKeyboardButton('My Token Balance',callback_data = 'show_balance')],[InlineKeyboardButton('Referral link',callback_data = 'show_referral')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message.reply('Menu:',reply_markup = reply_markup)
    '''else:
        message.reply('Hello [{}](tg://user?id={}),\nTo continue please solve the captcha below!'.format(firstname,user_id))
        gen_captcha(user_id)
        app.send_photo(chat_id = chat_id,photo = './captcha/{}.png'.format(str(user_id)))
        states[str(user_id)] = 'captcha_true'
'''
@app.on_message(Filters.command('menu'))
def show_menu_now1(client,message):
    try:
        level = userinfo[str(userid)+'_task_level']
        if level < 5:
            level = False
        else:
            level = True
    except:
        user = check_user
        if user:
            level = user[5]
            if level < 5:
                level = False
            else:
                level = True
        else:
            level = False
    if level:
        keyboard = [[InlineKeyboardButton('My Token Balance',callback_data = 'show_balance')],[InlineKeyboardButton('Referral link',callback_data = 'show_referral')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message.reply('Menu:',reply_markup = reply_markup)
    else:
        message.reply("You haven't yet completed all of the tasks to be able to see the menu please /start and complete all the tasks!")

@app.on_message(Filters.command('getmethecsv'))
def get_me_the_csv(client,message):
    user_id = message.from_user.id
    sql = 'Select * from users'
    a = db.execute(sql)
    b = a.fetchall()
    c = csv.writer(open('./users.csv', 'w'))
    for x in b:
      c.writerow(x)
    app.send_document(chat_id = chat_id, filename='./users.csv')
     
@app.on_message(captcha_filter)
def captcha_check(client,message):
    user_id = message.from_user.id
    chatid = message.chat.id
    text = message.text
    string = states[str(user_id)+'_captcha']
    if text == string:
        states[str(user_id)] = 'captcha_false'
        userinfo[str(user_id)+'_task_level'] = 2
        t = Thread(target = update_user,args=(user_id,'n','n',2,'n',))
        t.start()
        keyboard = [[InlineKeyboardButton("Join Group", url = 'https://t.me/medalte')],
                    [InlineKeyboardButton('Join Channel', url = 'https://t.me/medalteAnn')],
                    [InlineKeyboardButton('Done!', callback_data = 'verify_tg:{}'.format(user_id))]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message.reply('To be able to participate in the AirDrop you need to complete some tasks.\n\n Firstly join @medalte and @medalteAnn',reply_markup = reply_markup)
    else:
        message.reply('Wrong!! Please try again.')
        gen_captcha(user_id)
        app.send_photo(chat_id = chatid,photo = './captcha/{}.png'.format(str(user_id)))

@app.on_message(twitter_input_filter)
def twitter_input_now(client,message):
    user_id = message.from_user.id
    text = message.text
    userinfo[str(user_id)+'_twitter_username'] = message.text
    update_user(user_id,'n',text,4,'n')
    userinfo[str(user_id)+'_task_level'] = 4
    t = Thread(target = update_user,args=(user_id,'n','n',4,'n'))
    t.start()
    states[str(user_id)] = 'medium_wait_13'
    def change_wait_time(userid):
        n = 12
        while n >= 0:
            time.sleep(1)
            states[str(userid)] = 'medium_wait_{}'.format(n)
            n = n-1
    t = Thread(target = change_wait_time,args=(user_id,))
    t.start()
    keyboard = [[InlineKeyboardButton('Our medium page!',url = 'https://medium.com/@support_28864')],
        [InlineKeyboardButton("Done!", callback_data = 'verify_medium_time')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message.reply('Now visit our medium page and like/clap on any one of our posts!',reply_markup  = reply_markup)


@app.on_callback_query(tg_verify_filter)
def check_tg(_,query):
    userid = query.message.chat.id
    #print(query)
    print(userid)
    try:
        app.get_chat_member(medalte_group,userid)
        app.get_chat_member(medalte_channel,userid)
        userinfo[str(userid)+'_task_level'] = 3
        print('Done!!!!!')
        t = Thread(target = update_user,args=(userid,'n','n',3,'n',))
        t.start()
        states[str(userid)] = 'twitter_input'
        keyboard = [[InlineKeyboardButton('Visit Our twitter Page',url = 'https://twitter.com/medaltetoken')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text('The next task is to visit our twitter profile and follow us,retweet and share our pinned post \nThen Send your username to me without @',reply_markup = reply_markup)
    except:
        keyboard = [[InlineKeyboardButton("I've joined both!", callback_data = 'verify_tg:{}'.format(userid))]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text('Make Sure you have joined both @medalte and @medalteAnn !!',reply_markup = reply_markup)        
        
@app.on_callback_query(twitter_verify_filter)
def twitter_check_1(client,message):
    userid = message.from_user.id
    userinfo[str(userid)+'_task_level'] = 3
    t = Thread(target=update_user,args=(userid,'n','n',3,'n',))
    t.start()
    states[str(user_id)] = 'twitter_input'
    keyboard = [[InlineKeyboardButton('Visit Our twitter Page',url = 'https://twitter.com/medaltetoken')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('The next task is to visit our twitter profile and follow us,retweet and share our pinned post \nThen Send your username to me without @',reply_markup = reply_markup)

@app.on_callback_query(medium_verify_filter)
def medium_verify_now(_,query):
    userid = query.message.chat.id
    states[str(userid)] = 'medium_wait_13'
    def change_wait_time(userid):
        import time
        n = 12
        while n >= 0:
            time.sleep(1)
            states[str(userid)] = 'medium_wait_{}'.format(n)
            n = n-1
    t = Thread(target = change_wait_time,args=(usrid,))
    t.start()
    keyboard = [[InlineKeyboardButton('Our medium page!',url = 'https://medium.com/@support_28864')],
        [InlineKeyboardButton("Done!", callback_data = 'verify_medium_time')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('Now visit our medium page and like/clap on any one of our posts!',reply_markup  = reply_markup)
    
@app.on_callback_query(medium_verify_time_filter)
def medium_check_time(_,query):
    userid = query.message.chat.id
    ttime = states[str(userid)]
    if ttime == 'medium_wait_0':
        keyboard = [[InlineKeyboardButton("Menu", callback_data = 'show_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        userinfo[str(userid)+'_task_level'] = 5
        userinfo[str(userid)+'_balance'] = 50
        update_user(userid,50,'n',5,'n')
        query.edit_message_text("Congrats you've successfully participated into medalte airdrop and have got 50 MTDL tokens as a gift!\n\nUse your referral link below to earn more \n```https://t.me/medaltebot?start={}``` \n".format(userid),reply_markup=reply_markup)   

    else:
        keyboard = [[InlineKeyboardButton('Our medium page!',url = 'https://medium.com/@support_28864')],
            [InlineKeyboardButton("Done!", callback_data = 'verify_medium_time')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text('You did not like/clap on any of our medium posts please complete the task!',reply_markup = reply_markup)

@app.on_callback_query(menu_filter)
def show_menu_now(_,query):
    keyboard = [[InlineKeyboardButton('My Token Balance',callback_data = 'show_balance')],[InlineKeyboardButton('Referral link',callback_data = 'show_referral')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('Menu:',reply_markup = reply_markup)

@app.on_callback_query(balance_filter)
def show_balance(_,query):
    userid = query.message.chat.id
    try:
        bal = userinfo[str(userid)+'_balance']
    except:
        user = check_user(userid)
        bal = user[3]
        userinfo[str(userid)+'_balance'] = bal
    keyboard = [[InlineKeyboardButton('Back',callback_data = 'show_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('Hello your current token balance is {}'.format(bal),reply_markup = reply_markup)
    
@app.on_callback_query(show_referral_query)
def show_me_ref(_,query):
    userid = query.message.chat.id
    keyboard = [[InlineKeyboardButton('Back',callback_data = 'show_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('Your Referral link is \n\n```https://t.me/medaltebot?start={}```'.format(userid),reply_markup = reply_markup)
        
@app.on_callback_query(show_menu_filter)
def show_menu_now(_,query):
    keyboard = [[InlineKeyboardButton('My Token Balance',callback_data = 'show_balance')],[InlineKeyboardButton('Referral link',callback_data = 'show_referral')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('Menu:',reply_markup = reply_markup)
app.run()