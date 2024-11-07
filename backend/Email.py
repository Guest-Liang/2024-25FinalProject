import smtplib, yaml, os, logging, urllib.parse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
logger = logging.getLogger(__name__)

with open("./config/config.yaml", "r") as file:
    CONFIG_YAML = yaml.safe_load(file)


def SendEmailWithAttachment(
    sender_email,
    receiver_email,
    subject,
    body,
    password,
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
    From = CONFIG_YAML["Email"]["Account"]
    To = "GuestLiang@outlook.com"
    Subject = "Test Email From Python With Attachment"
    Body = """
    This email contains an attachment.
    Do not reply to this email. --- From Python 3.12.7
    """
    Password = CONFIG_YAML["Email"]["Password"]
    FilePaths = ["./backend/pic/1.png", "./backend/pic/2.png"]

    SendEmailWithAttachment(
        sender_email=From, 
        receiver_email=To, 
        subject=Subject, 
        body=Body, 
        password=Password, 
        file_paths=FilePaths
    )
