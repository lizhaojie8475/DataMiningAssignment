import pymysql

class MySqlHelper():

    def __init__(self, host="localhost", user="root", passwd="1111", db="datamining"):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db

    def connect(self):
        self.conn = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.db, charset="utf8")
        self.cur = self.conn.cursor()

    def search(self, sql):
        self.cur.execute(sql)
        res = self.cur.fetchall()
        return res

    def insert(self, sql, *args):
        self.cur.execute(sql, args)
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()
