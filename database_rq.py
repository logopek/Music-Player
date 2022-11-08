import sqlite3
import os

class Database(object):
    def __init__(self, database="media_db.db"):
        if not os.path.exists(os.path.dirname(__file__) +"\\" + database):
            open(database, "w")
            tempcon = sqlite3.connect(database)
            tempcon.cursor().execute("CREATE TABLE 'music' (path string(32767))")
            tempcon.commit()
            tempcon.close()
        self.con = sqlite3.connect(database)
        self.cur = self.con.cursor()

    def add_music(self, path):
        try:
            self.cur.execute("INSERT INTO 'music' VALUES ('{}')".format(path))
            self.con.commit()
        except Exception as e:
            print("No database found " + str(e))
            return ""

    def read_music(self):
        try:
            return self.cur.execute("SELECT * FROM 'music'").fetchall()
        except Exception as e:
            print("No database found " + str(e))
            return ""


    def request_select(self, sql_request):
        try:
            return self.cur.execute(sql_request).fetchall()
        except Exception as e:
            print("No database found " + str(e))
            return ""