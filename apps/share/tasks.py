from email.policy import default

from celery import shared_task
from celery.utils.log import  get_task_logger
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from core import settings
from twilio.rest import Client

logger = get_task_logger(__name__)

@shared_task
def send_sms_task(phone_number: str,otp_code: str):
    account_sid = settings.config("ACCOUNT_SID",default="")
    auth_token = settings.config("AUTH_TOKEN",default="")
    service_sid = settings.config("SERVICE_SID",default="")

    client = Client(account_sid,auth_token)

    try:
        message = client.messages.create(
            body=f"Your OTP code is {otp_code}",from_=service_sid,to=phone_number
        )
        print(f"Message SID: {message.sid}")
    except Exception as e:
        print(f"Error: {e}")


@shared_task
def send_email_task(email:str,otp_code:str):
    message = render_to_string(
        "emails/email_template.html",
        {
            "email":email,
            "otp_code":otp_code
        }
    )
    email_message = EmailMessage(
        "Your verification Code!",
        message,
        settings.EMAIL_HOST_USER,
        [email]
    )
    email_message.content_subtype = "html"
    try:
        print(f"OTP_CODE EMAIL:{otp_code}")
        email_message.send(fail_silently=False)
        return 200
    except Exception as e:
        print(f"Failed to send email: {e}")
        return 400