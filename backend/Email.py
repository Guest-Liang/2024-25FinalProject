import smtplib, yaml, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

with open("./config/config.yaml", "r") as file:
    CONFIG = yaml.safe_load(file)


def SendEmailWithAttachment(
    sender_email,
    receiver_email,
    subject,
    body,
    password,
    file_path=None,
    smtp_server="smtp.qq.com",
    smtp_port=587,
):
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    # Adding Message Body Content
    msg.attach(MIMEText(body, "plain"))

    # Process Attachment
    if file_path:
        filename = os.path.basename(file_path)
        attachment = open(file_path, "rb")

        # Construct MIMEBase object for attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= {filename}")

        msg.attach(part)
        attachment.close()

    # Connecting to SMTP Server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Enable secure connection
    try:
        server.login(sender_email, password)
        print("Login successful")

        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        print(f"Email sent to {receiver_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()  # Close the connection


if __name__ == "__main__":
    From = CONFIG["Email"]["Account"]
    To = "GuestLiang@outlook.com"
    Subject = "Test Email From Python With Attachment"
    Body = """
    This email contains an attachment.
    Do not reply to this email. --- From Python 3.12.7
    """
    Password = CONFIG["Email"]["Password"]
    FilePath = "./backend/pic/1.png"

    SendEmailWithAttachment(From, To, Subject, Body, Password, FilePath)
