#

import mysql.connector
import game_objects


if __name__ == "__main__":
    conn = mysql.connector.connect(
        host='localhost',
        database='htm_database',
        user='htm',
        password='play',
        autocommit=True
    )

    player = game_objects.Player('Player 1', 250, 1000, 'KBOS')
    musk = game_objects.Player('Elon Musk', 1000000, 9999999, 'KBOI', game_objects.Airplane('Air Force Musk'))
    
    conn.close()


# Test
'''query = f'SELECT * FROM minigame WHERE difficulty = 2'
cur = conn.cursor()
cur.execute(query)
results = cur.fetchall()

for row in results:
    print(row)'''
# Test end