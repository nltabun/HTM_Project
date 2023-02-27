#
import mysql.connector
import game_init



def load_player_data(connection):
    query = f'SELECT * FROM game ORDER BY id DESC'
    cur = connection.cursor()
    cur.execute(query)
    result = cur.fetchall()

    planes = game_init.generate_airplanes()
    print(result[0])
    print(result[1])
    #return r


def save_player_data(connection):
    pass


if __name__ == "__main__":
    conn = mysql.connector.connect(
        host='localhost',
        database='htm_database',
        user='htm',
        password='play',
        autocommit=True
    )

    load_player_data(conn)