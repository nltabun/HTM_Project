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

# Start config
# Player money (TSLA Stock), fuel reserve & default plane index
player_money = 500
player_fuel = 50000
player_plane = 1
# Musk money (TSLA Stock), fuel reserve & plane index
musk_money = 1000000 
musk_fuel = 9999999
musk_plane = 0

# Game length
short_min = 15
short_max = 20
long_min = 30
long_max = 40 