import smtplib
from pathlib import Path

from PIL import Image
from pydantic import EmailStr

from app.config import settings
from app.tasks.celery import celery
from app.tasks.email_templates import create_booking_confirmation_template


@celery.task
def process_pic(
    path: str,
):
    image_path = Path(path)
    image = Image.open(image_path)
    image_resized_large = image.resize((1000, 500))
    image_resized_small = image.resize((200, 100))
    image_resized_large.save(
        f'app/static/images/large_{image_path.name}'
    )
    image_resized_small.save(
        f'app/static/images/small_{image_path.name}'
    )


@celery.task
def send_booking_confirmation_email(
    booking: dict,
    recipient: EmailStr
):
    msg_content = create_booking_confirmation_template(booking, recipient)
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)
