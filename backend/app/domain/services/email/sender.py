# import smtplib
# from email.mime.text import MIMEText

# from app.core.config import settings

# SMTP_SERVER = settings.SMTP_SERVER
# SMTP_PORT = settings.SMTP_PORT
# SMTP_USERNAME = settings.SMTP_USERNAME
# SMTP_PASSWORD = settings.SMTP_PASSWORD


# def send_verification_email(to_email: str, token: str):
#     subject = "Verify Your Email"
#     verification_link = f"{settings.FRONTEND_URL}/verify-email?token={token}"
#     body = f"Click the link to verify your email: {verification_link}"

#     msg = MIMEText(body)
#     msg["Subject"] = subject
#     msg["From"] = SMTP_USERNAME
#     msg["To"] = to_email

#     with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
#         server.starttls()
#         server.login(SMTP_USERNAME, SMTP_PASSWORD)
#         server.sendmail(SMTP_USERNAME, to_email, msg.as_string())
