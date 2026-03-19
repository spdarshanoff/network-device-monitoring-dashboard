from database.db_connection import get_connection


def get_device_stats(device_id):

    conn = get_connection()
    cursor = conn.cursor()

    # total checks

    cursor.execute(
        "SELECT COUNT(*) FROM logs WHERE device_id=%s",
        (device_id,)
    )

    total = cursor.fetchone()[0]

    # uptime

    cursor.execute(
        "SELECT COUNT(*) FROM logs WHERE device_id=%s AND status='UP'",
        (device_id,)
    )

    up = cursor.fetchone()[0]

    # downtime

    cursor.execute(
        "SELECT COUNT(*) FROM logs WHERE device_id=%s AND status='DOWN'",
        (device_id,)
    )

    down = cursor.fetchone()[0]

    # avg latency

    cursor.execute(
        "SELECT AVG(latency) FROM logs WHERE device_id=%s",
        (device_id,)
    )

    avg_latency = cursor.fetchone()[0]

    if total == 0:
        uptime_percent = 0
    else:
        uptime_percent = (up / total) * 100

    conn.close()

    return {
        "total": total,
        "up": up,
        "down": down,
        "uptime_percent": uptime_percent,
        "avg_latency": avg_latency
    }


if __name__ == "__main__":

    stats = get_device_stats(1)

    print(stats)