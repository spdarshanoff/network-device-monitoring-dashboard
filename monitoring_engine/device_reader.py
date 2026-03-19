from database.db_connection import get_connection

def get_devices():

    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM devices"

    cursor.execute(query)

    devices = cursor.fetchall()

    conn.close()

    return devices

if __name__ == "__main__":

    data = get_devices()

    for d in data:
        print(d)