import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Msdhoni@7",
        database="network_monitor"
    )
    return conn
