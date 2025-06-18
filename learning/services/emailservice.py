from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

conf = ConnectionConfig(
    MAIL_USERNAME="aman12bhatnagar@gmail.com",
    MAIL_PASSWORD="ofynvknrrhxykdmv",
    MAIL_FROM="aman12bhatnagar@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,      # Gmail uses STARTTLS on port 587
    MAIL_SSL_TLS=False,      # Should be False for STARTTLS
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER=None,
)

async def send_welcome_email(email_to: str, username: str):
    subject = "Welcome to Our Service!"

    body = f"""
    Dear {username},

    Welcome to Our Service!

    We are delighted to have you on board. Thank you for registering with us. 
    Our team is committed to providing you with the best experience possible.

    If you have any questions or need assistance, please do not hesitate to reach out to our support team.

    Best regards,
    The Team at Our Service
    """

    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=body.strip(),
        subtype="plain"
    )
    fm = FastMail(conf)
    await fm.send_message(message)