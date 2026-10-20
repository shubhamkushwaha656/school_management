
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="shubham",
    password="abc123",
    database="school_management"
)

print("Database connected successfully")


