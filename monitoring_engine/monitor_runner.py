from monitoring_engine.device_reader import get_devices
from monitoring_engine.ping_checker import check_ping
from monitoring_engine.health_engine import update_score

from database.db_connection import get_connection
from datetime import datetime


def run_monitor():

    devices = get_devices()

    conn = get_connection()
    cursor = conn.cursor()

    for d in devices:

        device_id = d[0]
        name = d[1]
        ip = d[2]

        status, latency = check_ping(ip)

        print("-----")
        print("Device:", name)
        print("IP:", ip)
        print("Status:", status)
        print("Latency:", latency)

        # Insert log

        log_query = """
        INSERT INTO logs
        (device_id, status, latency, check_time)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            log_query,
            (
                device_id,
                status,
                latency,
                datetime.now()
            )
        )

        # Update health score

        update_score(
            device_id,
            status,
            latency
        )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    run_monitor()