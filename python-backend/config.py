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

# Exclude from start locations
invalid_starts = 'WHERE NOT ident = \'PHNL\' AND NOT ident = \'PANC\' AND NOT ident = \'CYYT\''

# High risk locations
high_risk = {'KDTW','KSTL','KORD','MHPR','MMMX','MMGL','MHSC','MMMY','MMHO','MGGT','MMTG'}
cartel_risk = {'MHPR','MMMX','MMGL','MHSC','MMMY','MMHO','MGGT','MMTG'}

# Weather api
api_key = 'f08355556ae585e753c3498c6cc4756c'
bad_weather = {'200','201','202','210','211','212','221','230','231','232',
               '302','312','314','502','503','504','522','531','602','622',
               '701','711','721','731','741','751','761','762','771','781'}
weather_fallback = {
                    "status" : 1,
                    "temperature" : 10.1,
                    "weather_desc" : 'broken clouds',
                    "wind_speed" : 2.2,
                    "visibility" : 10000
                }