import pymysql.cursors
host = "104.223.107.42"
user = 'amit'
password = 'amitpandey123121'
db1 = 'airdropbot'
#host = 'localhost'
new_user_busy = 0
new_group_busy = 0
update_user_busy = 0
update_group_busy = 0

class DB:
    conn = None
    def connect(self):
        self.conn = pymysql.connect(host = host,user = user,password = password,db = db1)
    def execute(self, sql):
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

db = DB()
#db_con = pymysql.connect(host = host,user = user,password = password,db = db)

    
def check_connection(conn):
    def check_db_connection(conn):
        if conn:
            return True
        else:
            try:
                conn =  connect(host = "104.223.107.42",user = "amit",password = "amitpandey123121",db = "covid19bot")
                return True
            except:
                return False
    return check_db_connection(conn)
def create_user(userid,refby):
    if refby!='n':
        sql = 'Insert into users(userid,referred_by) values({},{})'.format(userid,refby)
    else:
        sql = 'Insert into users(userid) values({})'.format(userid)
    db.execute(sql)
    db.commit()

def check_user(userid):
    userid = str(userid)
    sql = 'Select * from users where userid = {}'.format(userid)
    a = db.execute(sql)
    try:
        r = a.fetchall()
    except AttributeError:
        r =None
    if r:
        return r[0]
    else:
        return False
    

def update_user(userid,balance,twitter_username,task_level,total_referrals):
    sql = 'Update users SET '
    a = ' Where userid = {}'.format(userid)
    if balance != 'n':
        if (twitter_username != 'n') or (task_level!='n') or (total_referrals != 'n'):
            sql = sql + "balance = {}, ".format(balance)
        else:
            sql = sql + "balance = {}".format(balance)
    if twitter_username != 'n':
        if (task_level != 'n') or (total_referrals != 'n'):
            sql = sql+"twitter_username = '{}', ".format(twitter_username)
        else:
            sql = sql+"twitter_username = '{}'".format(twitter_username)
    if task_level != 'n':
        if total_referrals != 'n':
            sql = sql+'task_level = {}, '.format(task_level)
        else:
            sql = sql+'task_level = {}'.format(task_level)
    if total_referrals != 'n':
        sql = sql+'total_referrals = {}'.format(total_referrals)
    sql = sql+a
    db.execute(sql)
    db.commit()

def new_ref(refby,refto):
    sql = "Insert into referral(refby,refto) values({},{})".format(str(refby),str(refto))
    db.execute(sql)
    db.commit()
    user = check_user(refby)
    total = user[6]
    total = total+1
    sql = "Update users Set total_referrals = {} where userid={}".format(total,refby)
    db.execute(sql)
    db.commit()
    