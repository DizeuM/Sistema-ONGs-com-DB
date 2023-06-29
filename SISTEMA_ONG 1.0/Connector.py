import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="ong_x"
)

mycursor = mydb.cursor()