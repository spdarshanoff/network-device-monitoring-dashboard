from database.db_connection import get_connection
from datetime import datetime
from monitoring_engine.alert_engine import create_alert


def get_failure_count(device_id, cursor):

    query = """
    SELECT status
    FROM logs
    WHERE device_id=%s
    ORDER BY log_id DESC
    LIMIT 3
    """

    cursor.execute(query, (device_id,))
    rows = cursor.fetchall()

    count = 0

    for r in rows:
        if r[0] == "DOWN":
            count += 1

    return count


def get_health_status(score):

    if score >= 80:
        return "HEALTHY"

    elif score >= 50:
        return "DEGRADING"

    else:
        return "CRITICAL"


def update_score(device_id, status, latency):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT score FROM health_score WHERE device_id=%s",
        (device_id,)
    )

    row = cursor.fetchone()

    if row is None:
        score = 100
    else:
        score = row[0]

    if status == "UP":
        score += 2
    else:
        score -= 5

    if latency is not None and latency > 100:
        score -= 5

    failure_count = get_failure_count(device_id, cursor)

    if failure_count >= 3:
        score -= 15

    if score > 100:
        score = 100

    if score < 0:
        score = 0

    health_status = get_health_status(score)

    # create alert
    create_alert(device_id, health_status)

    cursor.execute(
        """
        INSERT INTO health_score
        (device_id, score, health_status, last_update)
        VALUES (%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE
        score=%s,
        health_status=%s,
        last_update=%s
        """,
        (
            device_id,
            score,
            health_status,
            datetime.now(),
            score,
            health_status,
            datetime.now()
        )
    )

    conn.commit()
    conn.close()