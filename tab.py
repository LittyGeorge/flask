
import sqlite3

conn = sqlite3.connect('task.db')
conn.execute('CREATE TABLE IF NOT EXISTS users(userid INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT NOT NULL UNIQUE,password TEXT NOT NULL,usertype TEXT NOT NULL,is_approve BOOLEAN)')
conn.execute('CREATE TABLE IF NOT EXISTS stud(studid INTEGER PRIMARY KEY AUTOINCREMENT,firstname TEXT,lastname TEXT,phno INTEGER,age INTEGER,userid INTEGER,FOREIGN KEY (userid) REFERENCES users(userid))')
conn.execute('CREATE TABLE IF NOT EXISTS teacher(teachid INTEGER PRIMARY KEY AUTOINCREMENT,firstname TEXT,lastname TEXT,phno INTEGER,age INTEGER,userid INTEGER,FOREIGN KEY (userid) REFERENCES users(userid))')

print("successfully connected")
