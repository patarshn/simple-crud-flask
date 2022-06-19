import mysql.connector

try:
  con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mig_db",
    autocommit=True,
  )
except Exception as e:
  print(e)
  exit(0)

cur = con.cursor(dictionary=True,buffered= True)