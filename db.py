import pymysql.cursors

#host = 'us-cdbr-iron-east-01.cleardb.net'
#user = 'bda23286c6fc69'
#password = '92202601'
#dab = 'heroku_6460cd56c207d37'
'''blueprnt:
users:
id
userid

'''
host = '104.223.107.42'
user = 'root'
password = 'amitpandey123121'
dab = 'airdropbot'

class DB:
    conn = None
    def connect(self):
        #self.conn = pymysql.connect(host = host,user = "amit",password = "amitpandey123121",db = "covid19bot")
        self.conn = pymysql.connect(host = host,user = user,password = password,db = dab)
    def query(self, sql):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
        except:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(sql)
        return cursor
    def commit(self):
        try:
            self.conn.commit()
        except:
            self.connect()
            self.conn.commit()
    def rollback(self):
        try:
            self.conn.rollback()
        except:
            self.connect()
            self.conn.rollback()


db = DB()

def create_user(userid,refby):
    if refby!='n':
        sql = 'Insert into users(userid,referred_by) values({},{})'.format(userid,refby)
    else:
        sql = 'Insert into users(userid) values({})'.format(userid)
    db.query(sql)
    db.commit()

def check_user(userid):
    sql = 'Select * from users where userid = {}'.format(str(userid))
    a = db.query(sql)
    r = a.fetchall()
    if r:
        return r[0]
    else:
        return False

def update_user(userid,balance,twitter_username,task_level):    
    sql = 'Update users SET '
    a = ' Where userid = {}'.format(userid)
    if balance != 'n':
        if (twitter_username != 'n') or (task_level!='n'):
            sql = sql + "balance = {}, ".format(str(balance))
        else:
            sql = sql + "balance = {}".format(str(balance))
    if twitter_username != 'n':
        if task_level != 'n':
            sql = sql+"twitter_username = '{}', ".format(twitter_username)
        else:
            sql = sql+"twitter_username = '{}'".format(twitter_username)
    if task_level != 'n':
        sql = sql+'task_level = {}'.format(str(task_level))
    sql = sql+end
    db.query(sql)
    db.commit()

def new_ref(refby,refto):
    sql = "Insert into referral(refby,refto) values({},{})".format(str(refby),str(refto))
    db.query(sql)
    db.commit()
    
    

            