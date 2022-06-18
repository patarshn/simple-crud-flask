import mysql.connector
import time

try:
    con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mig_db",
    #   autocommit=True
    )
except Exception as e:
    print(e)
    exit()

#Create a Connection
cur = con.cursor()


print("Migration users table")
cur.execute("DROP TABLE IF EXISTS users")
sql ='''CREATE TABLE users (
	users_id    int primary key not null auto_increment,
	username	varchar(255),
	password	varchar(255),
    role    varchar(30),
    created_at  datetime,
    deleted_at  datetime
);'''
cur.execute(sql)
con.commit()


print("Migration users absensis")
cur.execute("DROP TABLE IF EXISTS absensis")
sql ='''CREATE TABLE absensis (
	absensis_id	int primary key not null auto_increment,
	user_id int,
	check_in	datetime,
    check_out	datetime,
    created_at  datetime,
    deleted_at  datetime,
    CONSTRAINT absensis_user_id_fk FOREIGN KEY(user_id) REFERENCES users(users_id)
)'''
cur.execute(sql)
con.commit()


print("Migration users aktivitass")
cur.execute("DROP TABLE IF EXISTS aktivitass")
sql ='''CREATE TABLE aktivitass (
	aktivitass_id   int primary key not null auto_increment,
    user_id	int,
	nama_aktivitas	varchar(255),
	tanggal_aktivitas	date,
    waktu_aktivitas	time,
    status_aktivitas enum('on-going','finished'),
    created_at  datetime,
    deleted_at  datetime,
    CONSTRAINT aktivitass_user_id_fk FOREIGN KEY(user_id) REFERENCES users(users_id)
);'''
cur.execute(sql)
con.commit()

cur.close()
