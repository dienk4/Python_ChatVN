import  sqlite3
def register():
    conn = sqlite3.connect('dangky.db')
    print("ket noi thanh cong den csdl")
    conn.execute('DROP TABLE IF EXISTS dangky')
    conn.execute('''CREATE TABLE dangky
                (name TEXT NOT NULL,
                user TEXT PRIMARY KEY NOT NULL,
                SDT     INT NOT NULL,
                email     TEXT NOT NULL,
                pass      CHAR(30));''')
    print("Tao bang thanh cong")
    conn.close()
register()