import csv

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


def export_csv():

    conn = get_connection()
    cursor = conn.cursor()

    devices = get_all_devices()

    file = open("report.csv", "w", newline="")

    writer = csv.writer(file)

    writer.writerow([
        "Device",
        "IP",
        "Total",
        "Up",
        "Down",
        "Uptime%",
        "AvgLatency",
        "Score",
        "Health"
    ])

    for d in devices:

        device_id = d[0]
        name = d[1]
        ip = d[2]

        stats = get_device_stats(device_id)

        score, health = get_health(device_id, cursor)

        writer.writerow([
            name,
            ip,
            stats["total"],
            stats["up"],
            stats["down"],
            stats["uptime_percent"],
            stats["avg_latency"],
            score,
            health
        ])

    file.close()
    conn.close()

    print("CSV report created")


if __name__ == "__main__":

    export_csv()