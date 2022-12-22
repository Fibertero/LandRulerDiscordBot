import sqlite3

def startBot(botName):
    print(f"We have logged in as {botName}")

    db = sqlite3.connect('data.db')
    cur = db.cursor()

    #creating the table
    cur.execute('''CREATE TABLE IF NOT EXISTS players(username text NOT NULL, id integer NOT NULL)''')
    db.commit()
    db.close()