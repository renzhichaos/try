import pymysql

db = pymysql.Connect("localhost", "root", "root", "test")
cursor = db.cursor()