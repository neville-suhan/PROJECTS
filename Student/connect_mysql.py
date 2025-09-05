import mysql.connector

conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="123456",
    database="student_db",
    auth_plugin='mysql_native_password'  # 👈 Important
)
cursor = conn.cursor()
cursor.execute("SELECT * FROM students")

for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()
