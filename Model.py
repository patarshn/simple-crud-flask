import mysql.connector

con = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="mig_db",
  autocommit=True,
)

cur = con.cursor(dictionary=True,buffered= True)