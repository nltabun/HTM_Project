import mysql.connector

# Database connection
conn = mysql.connector.connect(
    user="rikuhel",
    password="1234",
    host="mysql.metropolia.fi",
    port=3306,
    database="rikuhel",
    autocommit=True
)