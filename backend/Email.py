import smtplib, os, logging, urllib.parse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from django.conf import settings
from Configs import CONFIG

logger = logging.getLogger(__name__)

def SendEmailWithAttachment(
    receiver_email,
    sender_email = CONFIG["Email"]["Account"],
    subject = "Email From Django Restful API backend",
    body = f"""
    Do not reply to this email.
    If you received this email by mistake, it may be because our users have entered the wrong email address, please ignore it.
    --- From {CONFIG["API"]["AppName"]} {CONFIG["API"]["Version"]}
    """,
    password=CONFIG["Email"]["Password"],
    file_paths=None,
    smtp_server="smtp.qq.com",
    smtp_port=587,
):
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    # Adding Message Body Content
    msg.attach(MIMEText(body, "plain"))

    if file_paths:
        for file_path in file_paths: 
            if os.path.isfile(file_path): 
                filename = os.path.basename(file_path)
                with open(file_path, "rb") as attachment:
                    # Construct MIMEBase object for attachment
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header("Content-Disposition", f"attachment; filename={urllib.parse.quote(filename)}")
                    msg.attach(part)
            else:
                logger.warning(f"File not found: {file_path}")

    # Connecting to SMTP Server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls() 
    try:
        server.login(sender_email, password)
        logger.info("Login successful")

        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        logger.info(f"Email sent to {receiver_email}")
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
    finally:
        server.quit()


if __name__ == "__main__":
    From = CONFIG["Email"]["Account"]
    To = "1736331027@qq.com"
    Subject = "Email From Django Restful API backend"
    Password = CONFIG["Email"]["Password"]
    FilePaths = ["./backend/pic/3.png", "./backend/pic/4.png"]

    SendEmailWithAttachment(
        sender_email=From, 
        receiver_email=To, 
        subject=Subject,  
        password=Password, 
        file_paths=FilePaths
    )
