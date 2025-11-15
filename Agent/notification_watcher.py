import time
import mysql.connector
from notifier import send_alert

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="006655@Chitra",
        database="CPUMETRIC"
    )

last_id = 0

def check_new_alerts():
    global last_id
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT prediction_id, system_id, probability
        FROM Prediction_Log
        WHERE downtime_risk = 1
        ORDER BY prediction_id DESC
        LIMIT 1
    """)

    row = cur.fetchone()
    cur.close()
    conn.close()

    if row and row["prediction_id"] > last_id:
        last_id = row["prediction_id"]
        msg = f"Downtime Risk!\nSystem: {row['system_id']}\nProbability: {row['probability']}"
        send_alert(row["system_id"], msg)

if __name__ == "__main__":
    while True:
        check_new_alerts()
        time.sleep(5)
