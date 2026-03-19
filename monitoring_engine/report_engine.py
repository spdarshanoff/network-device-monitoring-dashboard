from database.db_connection import get_connection
from monitoring_engine.analytics_engine import get_device_stats


def get_all_devices():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM devices")

    devices = cursor.fetchall()

    conn.close()

    return devices


def get_health(device_id, cursor):

    cursor.execute(
        "SELECT score, health_status FROM health_score WHERE device_id=%s",
        (device_id,)
    )

    row = cursor.fetchone()

    if row is None:
        return 0, "UNKNOWN"

    return row[0], row[1]


def generate_report():

    conn = get_connection()
    cursor = conn.cursor()

    devices = get_all_devices()

    print("\n===== DEVICE REPORT =====\n")

    for d in devices:

        device_id = d[0]
        name = d[1]
        ip = d[2]

        stats = get_device_stats(device_id)

        score, health = get_health(device_id, cursor)

        print("-----")
        print("Device:", name)
        print("IP:", ip)

        print("Total checks:", stats["total"])
        print("Uptime:", stats["up"])
        print("Downtime:", stats["down"])

        print("Uptime %:", stats["uptime_percent"])
        print("Avg latency:", stats["avg_latency"])

        print("Score:", score)
        print("Health:", health)

    conn.close()


if __name__ == "__main__":

    generate_report()