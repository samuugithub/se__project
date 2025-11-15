import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import mysql.connector
from plyer import notification
from twilio.rest import Client

# ----------------------------------------------------
# DB Connection
# ----------------------------------------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="006655@Chitra",
        database="CPUMETRIC"
    )

# ----------------------------------------------------
# Fetch admins
# ----------------------------------------------------
def get_admin_contacts():
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT name, email, phone FROM Admin")
        admins = cur.fetchall()
        cur.close()
        conn.close()
        return admins
    except:
        return []

# ----------------------------------------------------
# Email
# ----------------------------------------------------
def send_email(to_email, subject, body):
    sender = "dummy.alerts.system@gmail.com"
    password = "your_app_password_here"

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)
    except:
        pass

# ----------------------------------------------------
# WhatsApp
# ----------------------------------------------------
def send_whatsapp_message(to_number, message):
    try:
        client = Client("ACxxxx", "authxxxx")
        client.messages.create(
            body=message,
            from_="whatsapp:+14155238886",
            to="whatsapp:+91"+to_number
        )
    except:
        pass

# ----------------------------------------------------
# Popup notification
# ----------------------------------------------------
def show_system_notification(title, message):
    try:
        notification.notify(title=title, message=message, timeout=5)
    except:
        pass

# ----------------------------------------------------
# Main alert function
# ----------------------------------------------------
def send_alert(system_id, message):
    show_system_notification("System Alert", message)
    send_admin_notification(message)

def send_admin_notification(message):
    admins = get_admin_contacts()
    for adm in admins:
        if adm["email"]:
            send_email(adm["email"], "System Alert", message)
        if adm["phone"]:
            send_whatsapp_message(adm["phone"], message)
