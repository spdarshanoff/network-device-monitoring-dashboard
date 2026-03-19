from database.db_connection import get_connection
from datetime import datetime


def create_alert(device_id, health_status):

    conn = get_connection()
    cursor = conn.cursor()

    if health_status == "CRITICAL":
        alert_type = "CRITICAL"
        message = "Device is in critical state"

    elif health_status == "DEGRADING":
        alert_type = "WARNING"
        message = "Device performance degrading"

    else:
        return

    query = """
    INSERT INTO alerts
    (device_id, alert_type, message, alert_time)
    VALUES (%s,%s,%s,%s)
    """

    cursor.execute(
        query,
        (
            device_id,
            alert_type,
            message,
            datetime.now()
        )
    )

    conn.commit()
    conn.close()