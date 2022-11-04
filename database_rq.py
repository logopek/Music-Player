import sqlite3

class Database(object):
    def __init__(self, database="music_db.sqlite"):
        self.con = sqlite3.connect(database)
        self.cur = self.con.cursor()

    def add_music(self, path, title = "[]"):
            self.cur.execute("INSERT INTO 'music' VALUES ('{}', '{}')".format(path, title))
            self.con.commit()

    def read_music(self):
        return self.cur.execute("SELECT * FROM music").fetchall()


    def request_select(self, sql_request):
        return self.cur.execute(sql_request).fetchall()